# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
# cache 模块
from flask_cache import Cache
# css,js打包器
from flask_assets import Environment
from .assetsBundle import (
    login_css,
    main_css,
    main_js,
    home_css,
    home_js,
    vsimFlowerQuery_css,
    vsimFlowerQuery_js,
    probVsimFirstDict_css,
    probVsimFirstDict_js,
    vsimmanual_css,
    vsimmanual_js,
    muticountry140_css,
    muticountry140_js,
    jqwidgets_globle_js,
    uploadfiles_css,
    uploadfiles_js,
    new_vsim_test_info_css,
    new_vsim_test_info_js
)
# app config
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
cache = Cache()
assets_env = Environment()


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """

    :param config_name: 根据不同环境如测试环境、开发环境等进行app初始化设置
    :return: 返回app上下文
    """
    app = Flask(__name__)
    # config app from config.py
    app.config.from_object(config[config_name])
    # app ext init
    config[config_name].init_app(app)
    pagedown.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    # 各个模块打包模块路径声明
    assets_env.init_app(app)
    # jqwidgets-plus
    assets_env.register("jqwidgets_globle_js", jqwidgets_globle_js)
    # login -statics
    assets_env.register("login_css", login_css)
    assets_env.register("main_css", main_css)
    assets_env.register("main_js", main_js)
    # gsvchome-statics
    assets_env.register("home_css", home_css)
    assets_env.register("home_js", home_js)
    # vsimFlowerQuery-statics
    assets_env.register("vsimFlowerQuery_css", vsimFlowerQuery_css)
    assets_env.register("vsimFlowerQuery_js", vsimFlowerQuery_js)
    # probVsimFirstDict-statics
    assets_env.register("probVsimFirstDict_css", probVsimFirstDict_css)
    assets_env.register("probVsimFirstDict_js", probVsimFirstDict_js)
    # vsimmanual-statics
    assets_env.register("vsimmanual_css", vsimmanual_css)
    assets_env.register("vsimmanual_js", vsimmanual_js)
    # 140country-statics
    assets_env.register("muticountry140_css", muticountry140_css)
    assets_env.register("muticountry140_js", muticountry140_js)
    # new vsim infor table
    assets_env.register("new_vsim_test_info_css", new_vsim_test_info_css)
    assets_env.register("new_vsim_test_info_js", new_vsim_test_info_js)
    # 140country-statics
    assets_env.register("uploadfiles_css", uploadfiles_css)
    assets_env.register("uploadfiles_js", uploadfiles_js)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
