"""
@author: harumonia
@license: (C) Copyright 2021, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@file: normal.py
@time: 2021/1/23 12:24
@desc:
"""
import datetime
import os
import random
import secrets
import time
import uuid

from jinja2 import Template

from config.secure import SecureInfo


def generate_password(length=8):
    """
    生成随机密码
    Returns:

    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password


def gen_id():
    """
    返回一个随机生成的uuid
    Returns:

    """
    return uuid.uuid4().hex


def datetime_creator():
    """
    返回标准格式的datetime
    Returns:

    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def datetime_creator_continuation():
    """
    返回连续格式的datetime
    Returns:

    """
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


# def pypinyin_dic():
#     from pypinyin import lazy_pinyin
#     from config.settings import xing_list, wei_list, guijing_list, \
#         shengjiangfuc_list
#
#     def pinyin_parser(flag, ll):
#         return {flag + ''.join(lazy_pinyin(foo)): foo for foo in ll}
#
#     return pinyin_parser('xing_', xing_list) \
#         , pinyin_parser('wei_', wei_list), pinyin_parser(
#         'gj_', guijing_list), pinyin_parser('sjfc_', shengjiangfuc_list)


def generate_mail_html(password="", port="", server="", runtime=""):
    """

    Args:
        runtime:
        server:
        password:
        port:

    Returns:

    """
    if password == "zxjzxj233":
        # 暂时隐藏真实密码
        password = "miaomiaomiao"
    pwd = f"<p>password:<strong>{password}</strong></p>"
    por = f"<p>port:<strong>{port}</strong></p>"
    ser = f"<p>server:<strong>{server}</strong></p>"
    rt = f"<p>runtime:<strong>{runtime}s</strong></p>"
    msg = "<p>NOTICE:service will auto exit after 3 days.</p>"
    result_info = pwd + por + ser + rt + msg
    """
    <table class="email-wraper"><tbody><tr><td class="py-5"><table class="email-header"><tbody><tr><td class="text-center pb-4"><a href="#"><img class="email-logo" src="/demo5/images/logo-dark2x.png" alt="logo"></a><p class="email-title">Conceptual Base Modern Dashboard Theme</p></td></tr></tbody></table><table class="email-body"><tbody><tr><td class="p-3 p-sm-5"><p><strong>Hello User</strong>,</p><p>Let's face it, sometimes you have a simple message that doesn’t need much design—but still needs flexibility and reliability. Select a basic email template. Write your message. Then send with confidence.</p><p>Its clean, minimal and pre-designed email template that is suitable for multiple purposes email template.</p><p>Hope you'll enjoy the experience, we're here if you have any questions, drop us a line at info@yourwebsite.com anytime. </p><p class="mt-4">---- <br> Regards<br>Abu Bin Ishtiyak</p></td></tr></tbody></table><table class="email-footer"><tbody><tr><td class="text-center pt-4"><p class="email-copyright-text">Copyright © 2020 DashLite. All rights reserved. <br> Template Made By <a href="https://themeforest.net/user/softnio/portfolio">Softnio</a>.</p><ul class="email-social"><li><a href="#"><img src="/demo5/images/socials/facebook.png" alt=""></a></li><li><a href="#"><img src="/demo5/images/socials/twitter.png" alt=""></a></li><li><a href="#"><img src="/demo5/images/socials/youtube.png" alt=""></a></li><li><a href="#"><img src="/demo5/images/socials/medium.png" alt=""></a></li></ul><p class="fs-12px pt-4">This email was sent to you as a registered member of <a href="https://softnio.com">softnio.com</a>. To update your emails preferences <a href="#">click here</a>.</p></td></tr></tbody></table></td></tr></tbody></table>
    """
    path = os.path.join(os.getcwd(), "application", "templates", "email_template.html")
    with open(path, "r") as f:
        html_tmp = f.read()
    t = Template(html_tmp)
    res = t.render(result_status="success", result_info=result_info)
    return res


def send_mail(
    receivers=None,
    html: str = "",
    subject: str = "",
    mail_host: str = "smtp.163.com",
    mail_user: str = "",
    mail_pass: str = "",
    mail_port: int = 465,
    file_content=None,
):
    """
    Send mail.
    Read necessary configuration from config.py.
    The mean of each argument can be found in README.md.
    Args:
        receivers: a list in which store receivers` email address. such as [zxjlm233@gamil.com].
        file_content: a BytesIO type. Because when send email, mori also send a CSV file of detail result.
                    The content is not absolutely generated but read from the workbook of xlwt.
        html: it`s a html5 table of CSV, for more intuitive display.
        subject: literal meaning
        mail_host: literal meaning
        mail_user: username of mail sender.
        mail_pass: password of mail senders.
        mail_port: depend on your service.

    Returns:
        None

    Notes: It`s a universal function can use in other scene by a little modification.
    """
    if receivers is None:
        receivers = ["zxjlm233@163.com"]

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender = SecureInfo.get_mail_user()
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ";".join(receivers)
    message["Subject"] = subject

    if html:
        message.attach(MIMEText(html, "html", "utf-8"))

    # part = MIMEText(file_content.getvalue(), "vnd.ms-excel", 'utf-8')
    # part.add_header('Content-Disposition', 'attachment',
    #                 filename=f'{subject}.xls')
    # message.attach(part)

    for _ in range(4):
        # try:
        if mail_port == 0:
            smtp = smtplib.SMTP()
            smtp.connect(mail_host)
        else:
            smtp = smtplib.SMTP_SSL(mail_host, mail_port)
        smtp.ehlo()
        smtp.login(SecureInfo.get_mail_user(), SecureInfo.get_mail_passwd())
        smtp.sendmail(sender, receivers, message.as_string())
        smtp.close()
        break
        # except Exception as _e:
        #     print(_e)
        #     if count == 3:
        #         raise Exception('failed to send email')


def get_random_color():
    """
    选择随机的颜色值
    Returns:

    """
    color_list = [
        "azure",
        "blue",
        "dark",
        "gray",
        "orange",
        "pink",
        "purple",
        # 'white',
        "gold",
        "green",
        "silver",
    ]
    return random.choice(color_list)


def get_time_delta(pre_date: datetime):
    """
    获取给定时间与当前时间的差值
    Args:
        pre_date:

    Returns:

    """
    date_delta = datetime.datetime.now() - pre_date
    return date_delta.days


def unique_list_dict_via_one_key(keyword, li):
    """
    为 list-dict 结构去重
    Args:
        keyword: 去重字段
        li: 需要去重的列表

    Returns:

    """
    return list({v[keyword]: v for v in li}.values())
