# coding: utf-8
from leancloud import Engine, Object, Query, LeanEngineError
from app import app

engine = Engine(app)


@engine.define
def rules(**params):
    if 'version' in params:
        version = params['version']
        if version >= "1.0":
            return rules_1_2()
        else:
            raise LeanEngineError(400, 'not supported version')
    else:
        raise LeanEngineError(400, 'params missing')

def rules_1_2():
    result = {
        "version": "",
        "safari": {
            "ads": {
                "general": [],
                "language": []
            },
            "analytics": [],
            "social": [],
            "font": []
        },
        "app": [],
        "video": []
    }

    safari_general_plugins = ["ads_general_block", "ads_general_hide"]
    safari_language_plugins = ["ads_lang_china_block", "ads_lang_china_hide"]
    safari_analytics_plugins = ["ads_analytics"]
    safari_social_plugins = ["ads_social"]
    safari_font_plugins = ["ads_font"]

    app_plugins = []
    video_plugins = []

    versions = []

    for plugin in safari_general_plugins:
        v = find_plugin(plugin, result['safari']['ads']['general'])
        if v:
            versions.append(v)

    for plugin in safari_language_plugins:
        v = find_plugin(plugin, result['safari']['ads']['language'])
        if v:
            versions.append(v)

    for plugin in safari_analytics_plugins:
        v = find_plugin(plugin, result['safari']['analytics'])
        if v:
            versions.append(v)

    for plugin in safari_social_plugins:
        v = find_plugin(plugin, result['safari']['social'])
        if v:
            versions.append(v)

    for plugin in safari_font_plugins:
        v = find_plugin(plugin, result['safari']['font'])
        if v:
            versions.append(v)

    for plugin in app_plugins:
        v = find_plugin(plugin, result['app'])
        if v:
            versions.append(v)

    for plugin in video_plugins:
        v = find_plugin(plugin, result['video'])
        if v:
            versions.append(v)
    if versions:
        result['version'] = max(versions)
    return result

def find_plugin(identifier, array):
    version = None
    query = Query(Rule)
    query.equal_to('identifier', identifier)
    query.descending("version")
    query.limit(1)
    rules_result = query.find()
    if rules_result:
        rule = rules_result[0].dump()
        rule['file'] = rule['file']['url']
        array.append(rule)
        version = rule['version']
    return version

class Rule(Object):

    @property
    def identifier(self):
        return self.get('identifier')

    @property
    def name(self):
        return self.get('name')

    @property
    def version(self):
        return self.get('version')

    @property
    def rule_file(self):
        return self.get('file')
