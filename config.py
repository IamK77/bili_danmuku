import yaml as yaml_origin
import os
import sys
from src.log import log_danmuku

rootpath = os.path.abspath(os.path.dirname(__file__))

logger = log_danmuku().logger


def get_config():
    global logger
    if os.path.exists('config.yaml'):
        with open(os.path.join(rootpath, 'config.yaml'), 'r', encoding='utf8') as f:
            config = yaml_origin.safe_load(f)
        logger = log_danmuku(DEBUG=config['DEBUG'], init=True).logger
        assert any(config['room_id']), "未填写房间号"
        for rid in config['room_id']:
            assert type(rid) is int, "房间号填写有误"
        conf_redis = config['redis']
        conf_mysql = config['mysql']
        assert type(conf_redis['port']) is int, "数据库端口号必须为int类型"
        assert type(conf_mysql['port']) is int, "数据库端口号必须为int类型"
        assert type(conf_redis['host']) is str, "数据库地址必须为字符串类型"
        assert type(conf_mysql['host']) is str, "数据库地址必须为字符串类型"
        assert type(conf_mysql['user']) is str, "MySQL数据库用户名必须为字符串类型"
        assert type(conf_mysql['password']) is str, "MySQL数据库密码必须为字符串类型"
        assert type(conf_mysql['database']) is str, "MySQL数据库database必须为字符串类型"
        assert type(conf_mysql['table_name']) is str, "MySQL数据库表名必须为字符串类型"
        logger.success('配置文件通过检查')
        str_room = [str(rid) for rid in config['room_id']]
        room_list = ', '.join(str_room)
        logger.success(f'预连接的直播间为: {room_list}')
        return config
    else:
        logger = log_danmuku().logger
        logger.warning('未检测到config.yaml文件')
        import ruamel.yaml
        generate_yaml = """\
        room_id: [510, 605, 21919321, 21452505]     # 按格式填写要监听的直播间号
# redis配置
        redis:     
            host: "localhost"
            port: 6379
            password: ""
# mysql配置
        mysql:      
            host: "localhost"
            port: 3306
            user: ""
            password: ""
            database: ""
            table_name: ""
# 设置禁词, 禁词将不会被写入数据库
        ban_msg: ['(⌒▽⌒)', '（￣▽￣）', '(=・ω・=)', '(｀・ω・´)', '(〜￣△￣)〜', '(･∀･)', '(°∀°)ﾉ', '(￣3￣)', '( ´_ゝ｀)', '→_→',
                        '(｀・ω・´)', '(･∀･)', '(>_>)', '("▔□▔)/', 'Σ(ﾟдﾟ;)', '(´；ω；`)', '(^・ω・^ )', '(●￣(ｴ)￣●)',
                        '(´･_･`)', '（￣へ￣）', 'ヽ(`Д´)ﾉ', '（#-_-)┯━┯', '( ゜- ゜)つロ', '✿ヽ(°▽°)ノ✿', '눈_눈', '_(≧∇≦」∠)_',
                        '✧(≖ ◡ ≖✿)', '(º﹃º )', '｡ﾟ(ﾟ´Д｀)ﾟ｡', '(┯_┯)', '( ๑ˊ•̥▵•)੭₎₎', 'Σ_(꒪ཀ꒪」∠)_', '(๑‾᷅^‾᷅๑)',
                        '打卡', '(●￣(ｴ)￣●).', '♡v♡', 'ε=ε=(ノ≧∇≦)ノ.', '⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄', '(￣3￣).', 'ε=ε=(ノ≧∇≦)ノ.']
        DEBUG: False    # 调试状态下为true, 默认不开启, 为false
        """
        yaml = ruamel.yaml.YAML()
        config = yaml.load(generate_yaml)

        with open(os.path.join(rootpath, 'config.yaml'), 'w', encoding='utf8') as f:
            yaml.dump(config, f)
        sys.exit('已生成config.yaml配置文件，请填写参数后重新运行')


conf = get_config()
logger = logger

if __name__ == '__main__':
    print(type(get_config()))
    print(rootpath)
