# spider_utils.py
import hashlib
import re

import html2text
import oss2
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import tempfile
import zipfile
import tarfile
import rarfile
import gzip
import shutil
import urllib
import ftfy
from loguru import logger
import pymysql
from .config import DB_CONFIG


def validate_and_fix_filename(filename):
    """
    校验文件名是否包含非法字符，若包含则进行修正
    :param filename: 待校验的文件名
    :return: 合法的文件名
    """
    # 定义非法字符的正则表达式
    illegal_char_regex = re.compile(r'[\\*?:"<>|]')
    # 定义替换非法字符的字符，这里使用下划线
    replacement_char = '_'

    # 检查文件名是否包含非法字符
    if illegal_char_regex.search(filename):
        # 若包含非法字符，将非法字符替换为指定的替换字符
        new_filename = illegal_char_regex.sub(replacement_char, filename)
        # print(f"原文件名 {filename} 包含非法字符，已修正为 {new_filename}")
        return new_filename
    return filename


class OSSManager:
    def __init__(self):
        self.security_token, self.access_key_id, self.access_key_secret = self.get_oss_credentials()
        self.bucket = self.initialize_oss_bucket(self.security_token, self.access_key_id, self.access_key_secret)

    def get_oss_credentials(self):
        # 链接
        conn = pymysql.connect(
            host="rm-2ze9f04i505y525i19o.mysql.rds.aliyuncs.com",
            port=3306,
            user="lucky2025",
            password="80f4%d5fc",
            db="patents",
            charset="utf8mb4"
        )
        # 获取到oss_sts表中的的数据
        sql_select = "select security_token,access_key_id, access_key_secret from oss_sts"
        cur = conn.cursor()
        cur.execute(sql_select)
        oss_sts = cur.fetchone()
        security_token = oss_sts[0]
        access_key_id = oss_sts[1]
        access_key_secret = oss_sts[2]
        conn.close()
        return security_token, access_key_id, access_key_secret

    def initialize_oss_bucket(self, security_token, access_key_id, access_key_secret):
        endpoint = 'oss-cn-beijing.aliyuncs.com'
        bucket_name = 'collect-datas'
        auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
        return oss2.Bucket(auth, endpoint, bucket_name)

    def upload_file_to_oss(self, file_content, oss_path):
        # exist = self.bucket.object_exists(oss_path)
        # if exist:
        #     print(f"文件 {oss_path} 已存在，链接为{self.get_file_url(oss_path)}跳过上传")
        #     return self.get_file_url(oss_path)
        result = self.bucket.put_object(oss_path, file_content)
        if result.status == 200:
            file_url = self.get_file_url(oss_path)
            print(f"文件 {oss_path} 上传到 OSS 成功，访问链接: {file_url}")
            return file_url
        else:
            logger.error(f"文件 {oss_path} 上传到 OSS 失败，状态码: {result.status}")

    def start_detect_file_type(self, item_id, response, file_name, file_url, table_name):
        if response.code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type:
                content_type = content_type.decode('utf-8')
                mime_type = content_type.split(';')[0].strip()
                if content_type and 'text/html' not in mime_type:
                    file_type = detect_file_type(file_name=file_name)
                    if not file_type:
                        file_name = get_filename_from_response(response)
                        file_type = detect_file_type(file_url=file_url, file_name=file_name)
                    supported_extensions = ('zip', 'tar', 'tar.gz', 'tgz', 'tar.bz2', 'tbz2', 'rar', 'gz')
                    if file_type in supported_extensions:
                        extracted_files = extract_archive(response.content, file_name)
                        for content, new_name in extracted_files:
                            valid_oss_filename = validate_and_fix_filename(new_name)
                            file_oss_url = self.upload_file_to_oss(content, valid_oss_filename)
                            file_size = len(content)
                            self.save_file_info(table_name, item_id, file_name, file_url, valid_oss_filename,
                                                file_oss_url,
                                                file_size,
                                                file_type)
                    else:
                        valid_oss_filename = validate_and_fix_filename(file_name)
                        file_oss_url = self.upload_file_to_oss(response.content, valid_oss_filename)
                        file_size = len(response.body)
                        self.save_file_info(table_name, item_id, file_name, file_url, valid_oss_filename, file_oss_url,
                                            file_size, file_type)
        else:
            logger.error(f"请求失败，状态码: {response.status}")

    def upload_file_from_html_to_oss(self, item_id, html, table_name):
        file_infos = extract_file_names(html)
        if file_infos:
            for file_info in file_infos:
                file_name = file_info['filename']
                file_url = file_info['href']
                is_valid = is_valid_url(file_url)
                if is_valid:
                    yield scrapy.Request(
                        file_url,
                        callback=self.start_detect_file_type,
                        meta={'item_id': item_id, 'file_name': file_name, 'file_url': file_url,
                              'table_name': table_name})

    def get_file_url(self, file_path):
        file_url = f"http://{self.bucket.bucket_name}.{self.bucket.endpoint.split('//')[1]}/{file_path}"
        return file_url

    def upload_html_to_oss(self, html, oss_object_name):
        file_url = self.get_file_url(oss_object_name)
        # exist = self.bucket.object_exists(oss_object_name)
        # if exist:
        #     print(f"文件 {oss_object_name} 已存在，链接为{file_url}跳过上传")
        #     return file_url
        result = self.bucket.put_object(oss_object_name, html)
        if result.status == 200:
            logger.info(f"html文件上传成功！OSS对象名称: {oss_object_name}, 文件OSS地址为: {file_url}")
            return file_url
        else:
            logger.error(f"html文件上传失败，状态码: {result.status}")
            raise Exception("html上传失败")


def calculate_md5(text):
    try:
        # 创建一个 MD5 哈希对象
        md5_hash = hashlib.md5()
        # 更新哈希对象的内容
        md5_hash.update(text.encode('utf-8'))
        # 获取十六进制表示的 MD5 哈希值
        md5_digest = md5_hash.hexdigest()
        return md5_digest
    except Exception as e:
        print(f"计算 MD5 时出现错误: {e}")
        return None


def save_markdown(site_name, html, item_name, md5_hash):
    oss_manager = OSSManager()
    name = site_name + "/" + md5_hash + '-' + item_name + ".md"
    new_name = validate_and_fix_filename(name).replace("&nbsp", '')
    converter = html2text.HTML2Text()  # 创建 html2text 转换器实例
    converter.ignore_links = False  # 不忽略链接
    # 转换 HTML 为 Markdown
    markdown = converter.handle(html)
    file_url = oss_manager.upload_html_to_oss(markdown, new_name)
    return file_url


def get_html(html, class_name=None, id=None):
    if class_name is None:
        return html
    soup = BeautifulSoup(html, 'html.parser')
    detail_elements = soup.find_all(class_=class_name, id=id)
    return str(detail_elements)


def extract_item_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    item_content = soup.get_text().replace("\xa0", '').replace("\n", '')
    return item_content
    # else:
    #     detail_elements = soup.find_all(class_=class_name, id=id)
    #     detail_texts = [element.get_text() for element in detail_elements]
    #     if not detail_texts:
    #         detail_elements = soup.find_all(class_='detail_Table')
    #         detail_texts = [element.get_text() for element in detail_elements]
    #     if detail_texts:
    #         iframe = detail_elements[0].find('iframe')
    #         if iframe:
    #             item_content = iframe['src']
    #             logger.info(f"iframe链接: {item_content}")
    #         else:
    #             item_content = detail_texts[0].replace("\xa0", '').replace("\n", '')
    #     else:
    #         item_content = ""
    #     return item_content


def extract_archive(archive_content, archive_name):
    temp_dir = tempfile.mkdtemp(prefix=f"extract_{archive_name}_")
    try:
        archive_path = os.path.join(temp_dir, archive_name)
        with open(archive_path, 'wb') as f:
            f.write(archive_content)
        archive_base_name = os.path.splitext(archive_name)[0]
        results = []
        if archive_name.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                for info in zip_ref.infolist():
                    if not info.is_dir():
                        content = zip_ref.read(info.filename)
                        try:
                            filename = info.filename.encode('cp437').decode('gbk')
                        except (UnicodeEncodeError, UnicodeDecodeError):
                            filename = info.filename
                        new_filename = f"{archive_base_name}/{filename}"
                        results.append((content, new_filename))
        elif archive_name.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2')):
            if archive_name.endswith('.tar'):
                mode = 'r'
            elif archive_name.endswith(('.tar.gz', '.tgz')):
                mode = 'r:gz'
            elif archive_name.endswith(('.tar.bz2', '.tbz2')):
                mode = 'r:bz2'
            with tarfile.open(archive_path, mode) as tar_ref:
                for member in tar_ref.getmembers():
                    if member.isfile():
                        content = tar_ref.extractfile(member).read()
                        try:
                            filename = member.name.encode('cp437').decode('gbk')
                        except (UnicodeEncodeError, UnicodeDecodeError):
                            filename = member.name
                        new_filename = f"{archive_base_name}/{filename}"
                        results.append((content, new_filename))
        elif archive_name.endswith('.rar'):
            with rarfile.RarFile(archive_path) as rar_ref:
                for file in rar_ref.infolist():
                    if not file.isdir():
                        content = rar_ref.read(file.filename)
                        try:
                            filename = file.filename.encode('cp437').decode('gbk')
                        except (UnicodeEncodeError, UnicodeDecodeError):
                            filename = file.filename
                        new_filename = f"{archive_base_name}/{filename}"
                        results.append((content, new_filename))
        elif archive_name.endswith('.gz'):
            try:
                with gzip.open(archive_path, 'rb') as f_in:
                    content = f_in.read()
                    out_file_name = os.path.splitext(archive_name)[0]
                    try:
                        filename = out_file_name.encode('cp437').decode('gbk')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        filename = out_file_name
                    new_filename = f"{archive_base_name}/{filename}"
                    results.append((content, new_filename))
            except Exception as e:
                logger.error(f"解压缩 GZ 文件 {archive_name} 时出错: {e}")
        else:
            logger.error(f"不支持的压缩包类型: {archive_name}")
        return results
    except Exception as e:
        logger.error(f"处理压缩包 {archive_name} 时出错: {e}")
        return []
    finally:
        shutil.rmtree(temp_dir)


def get_filename_from_response(response):
    cd = response.headers.get('Content-Disposition')
    if isinstance(cd, bytes):
        cd = cd.decode('utf-8')

    filename = None
    if cd:
        # 先尝试处理 filename*=
        if 'filename*=' in cd:
            parts = cd.split('filename*=')
            if len(parts) > 1:
                sub_parts = parts[1].split("''")
                if len(sub_parts) == 2:
                    encoded_filename = sub_parts[1]
                    filename = urllib.parse.unquote(encoded_filename)
        # 若 filename*= 未找到，再尝试处理 filename=
        elif 'filename=' in cd:
            parts = cd.split('filename=')
            if len(parts) > 1:
                filename_part = parts[1]
                # 处理可能的引号包裹
                if filename_part.startswith('"') and filename_part.endswith('"'):
                    filename = filename_part[1:-1]
                else:
                    # 若没有引号，直接使用
                    filename = filename_part
                try:
                    filename = urllib.parse.unquote(filename)
                except ValueError:
                    # 处理 URL 解码异常
                    print(f"URL 解码异常: {filename_part}")
                    filename = None
    # 若前面都没提取到文件名，从 URL 中提取
    if not filename:
        filename = urllib.parse.urlparse(response.url).path.split('/')[-1]

    # 使用 ftfy 修复文件名
    return ftfy.fix_text(filename) if filename else None


def detect_file_type(file_url=None, file_name=None):
    sources = []
    if file_url is not None:
        sources.append(urlparse(file_url).path)
    if file_name is not None:
        sources.append(file_name)

    for source in sources:
        if ext := os.path.splitext(source)[1].lower().strip('.'):
            return ext
    return ''


# def extract_file_names(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     # 查找 a 标签的 href 属性和 iframe 标签的 src 属性
#     link_tags = soup.find_all(['a', 'iframe'])
#     files = []
#     for tag in link_tags:
#         if tag.name == 'a':
#             link_attr = 'href'
#         elif tag.name == 'iframe':
#             link_attr = 'src'
#         href = tag.get(link_attr)
#         if not href:
#             continue
#         parsed_url = urlparse(href)
#         if parsed_url.scheme and parsed_url.netloc:
#             if tag.name == 'a':
#                 file_name = tag.get_text(strip=True)
#             elif tag.name == 'iframe':
#                 # 对于 iframe 标签，尝试从 src 中提取文件名
#                 file_name = href.split('/')[-1]
#             # 过滤文件名是链接地址的情况
#             if 'http' in file_name or 'https' in file_name:
#                 continue
#             file_name = file_name.strip()
#             # 判断 file_name 是否为 “原文链接地址”，如果不是则添加到列表中
#             if href and file_name and file_name != '原文链接地址' and file_name != '原文链接':
#                 files.append({'file_name': file_name, 'href': href})
#     return files

def extract_file_names(html_content, class_name=None):
    soup = BeautifulSoup(html_content, 'html.parser')
    if class_name:
        # 如果指定了 class_name，只在该 class 的元素内查找
        target_elements = soup.find_all(class_=class_name)
        if not target_elements:
            return []
        # 创建一个新的 BeautifulSoup 对象，只包含目标元素
        new_soup = BeautifulSoup(''.join(str(element) for element in target_elements), 'html.parser')
        link_tags = new_soup.find_all(['a', 'iframe'])
    else:
        # 如果没有指定 class_name，在整个 HTML 中查找
        link_tags = soup.find_all(['a', 'iframe'])
    files = []
    for tag in link_tags:
        if tag.name == 'a':
            link_attr = 'href'
        elif tag.name == 'iframe':
            link_attr = 'src'
        href = tag.get(link_attr)
        if not href:
            continue
        parsed_url = urlparse(href)
        if parsed_url.scheme and parsed_url.netloc:
            if tag.name == 'a':
                file_name = tag.get_text(strip=True)
            elif tag.name == 'iframe':
                # 对于 iframe 标签，尝试从 src 中提取文件名
                file_name = href.split('/')[-1]
            # 过滤文件名是链接地址的情况
            if 'http' in file_name or 'https' in file_name or 'www' in file_name or '.cn' in file_name:
                continue
            file_name = file_name.strip()
            # 判断 file_name 是否为 “原文链接地址”，如果不是则添加到列表中
            if (href and file_name and file_name != '原文链接地址'
                    and file_name != '原文链接' and file_name != "请到原网址下载附件" and file_name != "详情请见原网站"):

                files.append({'file_name': file_name, 'href': href})
    return files


def handle_error(failure):
    logger.error(f"请求出错: {failure.request.url}, 错误信息: {failure.value}")


def get_default_dict(table_name):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = cursor.fetchall()
            default_dict = {}
            for column in columns:
                field_name = column['Field']
                default_dict[field_name] = None
            return default_dict
    except pymysql.Error as e:
        logger.error(f"数据库操作出错: {e}")
        return None
    finally:
        conn.close()
# def save_html(item_number, html, item_name):
#     oss_manager = OSSManager()
#     html_name = item_number + '-' + item_name + ".txt"
#     file_url = oss_manager.upload_html_to_oss(html, html_name)
#     return file_url
