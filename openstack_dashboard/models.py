# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField, GroupedForeignKey

REVIEWER_INITIAL = 'I'
REVIEWER_AVAILABLE = 'A'
REVIEWER_SELECTED = 'S'
REVIEWER_UNAVAILABLE = 'N'
REVIEWER_STATE_CHOICE = (
    (REVIEWER_INITIAL, u"初始"),
    (REVIEWER_AVAILABLE, u"候选"),
    (REVIEWER_SELECTED, u"选中"),
    (REVIEWER_UNAVAILABLE, u"无法参加"),
)

REVIEW_STATE_NOTSTART = 'N'
REVIEW_STATE_ONGOING = 'O'
REVIEW_STATE_COMMITTED = 'F'
REVIEW_STATE_CHOICE = {
    REVIEW_STATE_NOTSTART: u"尚未开始",
    REVIEW_STATE_ONGOING: u"进行中",
    REVIEW_STATE_COMMITTED: u"已提交",
}

GENDER_CHOICE = (
    (u"男", u"男"),
    (u"女", u"女"),
)

ZHUANJIALEIXING_CHOICES = (
    (u"科技界专家", u"科技界专家"),
    (u"产业界专家", u"产业界专家"),
    (u"经济界专家", u"经济界专家"),
)

CHENGHAO_DEFAULT = u"无"
CHENGHAO_CHOICES = (
    (u"甘肃省领军人才第一层次", u"甘肃省领军人才第一层次"),
    (u"甘肃省领军人才第二层次", u"甘肃省领军人才第二层次"),
    (u"甘肃省特聘科技专家", u"甘肃省特聘科技专家"),
    (u"甘肃省优秀专家", u"甘肃省优秀专家"),
    (u"甘肃省优秀科技工作者", u"甘肃省优秀科技工作者"),
    (u"中国科学院院士", u"中国科学院院士"),
    (u"中国工程院院士", u"中国工程院院士"),
    (u"长江学者特聘教授", u"长江学者特聘教授"),
    (u"长江学者奖励计划人选", u"长江学者奖励计划人选"),
    (u"国务院政府特殊津贴专家", u"国务院政府特殊津贴专家"),
    (u"国家杰出青年科学基金获得者", u"国家杰出青年科学基金获得者"),
    (u"国家优秀青年科学基金获得者", u"国家优秀青年科学基金获得者"),
    (u"教育部“新世纪优秀人才支持计划”人选", u"教育部“新世纪优秀人才支持计划”人选"),
    (u"国家“千人计划”人选", u"国家“千人计划”人选"),
    (u"国家“百千万人才工程”人选", u"国家“百千万人才工程”人选"),
    (u"中科院“百人计划”人选", u"中科院“百人计划”人选"),
    (u"国家有突出贡献专家", u"国家有突出贡献专家"),
    (u"国家有突出贡献中青年专家", u"国家有突出贡献中青年专家"),
    (u"国家科技重大专项首席专家", u"国家科技重大专项首席专家"),
    (u"国家重大工程项目首席技术专家和管理专家", u"国家重大工程项目首席技术专家和管理专家"),
    (u"国家自然科学基金重大项目首席专家", u"国家自然科学基金重大项目首席专家"),
    (u"国家自然科学基金创新研究群体带头人", u"国家自然科学基金创新研究群体带头人"),
    (u"全国优秀科技工作者，教育部创新团队带头人", u"全国优秀科技工作者，教育部创新团队带头人"),
    (u"省级重点科技创新团队带头人", u"省级重点科技创新团队带头人"),
    (u"国家级科技奖励获得者", u"国家级科技奖励获得者"),
    (u"省级科技奖励获得者（二等奖以上）", u"省级科技奖励获得者（二等奖以上）"),
    (u"科技部科技领军人才", u"科技部科技领军人才"),
    (u"科技部中青年科技领军人才", u"科技部中青年科技领军人才"),
    (u"国家级重点实验室（工程技术中心）带头人", u"国家级重点实验室（工程技术中心）带头人"),
    (u"教育部重点实验室（工程技术中心）带头人", u"教育部重点实验室（工程技术中心）带头人"),
    (u"省级重点实验室（工程技术中心）带头人", u"省级重点实验室（工程技术中心）带头人"),
    (u"国际顶级学术期刊审稿人", u"国际顶级学术期刊审稿人"),
    (CHENGHAO_DEFAULT, u"无"),
    #(u"A1", u"甘肃省领军人才第一层次"),
    #(u"A2", u"甘肃省领军人才第二层次"),
    #(u"A3", u"甘肃省特聘科技专家"),
    #(u"A4", u"甘肃省优秀专家"),
    #(u"A5", u"甘肃省优秀科技工作者"),
    #(u"A6", u"中国科学院院士"),
    #(u"A7", u"中国工程院院士"),
    #(u"A8", u"长江学者特聘教授"),
    #(u"A9", u"长江学者奖励计划人选"),
    #(u"B1", u"国务院政府特殊津贴专家"),
    #(u"B2", u"国家杰出青年科学基金获得者"),
    #(u"B3", u"国家优秀青年科学基金获得者"),
    #(u"B4", u"教育部“新世纪优秀人才支持计划”人选"),
    #(u"B5", u"国家“千人计划”人选"),
    #(u"B6", u"国家“百千万人才工程”人选"),
    #(u"B7", u"中科院“百人计划”人选"),
    #(u"B8", u"国家有突出贡献专家"),
    #(u"B9", u"国家有突出贡献中青年专家"),
    #(u"C1", u"国家科技重大专项首席专家"),
    #(u"C2", u"国家重大工程项目首席技术专家和管理专家"),
    #(u"C3", u"国家自然科学基金重大项目首席专家"),
    #(u"C4", u"国家自然科学基金创新研究群体带头人"),
    #(u"C5", u"全国优秀科技工作者，教育部创新团队带头人"),
    #(u"C6", u"省级重点科技创新团队带头人"),
    #(u"C7", u"国家级科技奖励获得者"),
    #(u"C8", u"省级科技奖励获得者（二等奖以上）"),
    #(u"C9", u"科技部科技领军人才"),
    #(u"D1", u"科技部中青年科技领军人才"),
    #(u"D2", u"国家级重点实验室（工程技术中心）带头人"),
    #(u"D3", u"教育部重点实验室（工程技术中心）带头人"),
    #(u"D4", u"省级重点实验室（工程技术中心）带头人"),
    #(u"D5", u"国际顶级学术期刊审稿人"),
    #(u"NULL", u"无"),
)

# Follow iso-3166-1全球国家名称代码
COUNTRY_CHOICE = (
    ('CHN', u"中国（China）"),
    ('HKG', u"中国香港（Hong Kong, China）"),
    ('MAC', u"中国澳门（Macao, China）"),
    ('TWN', u"中国台湾（Taiwan, China）"),
    ('AND', u"安道尔（Andorra）"),
    ('ARE', u"阿联酋（United Arab Emirates）"),
    ('AFG', u"阿富汗（Afghanistan）"),
    ('ATG', u"安提瓜和巴布达（Antigua & Barbuda）"),
    ('AIA', u"安圭拉（Anguilla）"),
    ('ALB', u"阿尔巴尼亚（Albania）"),
    ('ARM', u"亚美尼亚（Armenia）"),
    ('AGO', u"安哥拉（Angola）"),
    ('ATA', u"南极洲（Antarctica）"),
    ('ARG', u"阿根廷（Argentina）"),
    ('ASM', u"美属萨摩亚（American Samoa）"),
    ('AUT', u"奥地利（Austria）"),
    ('AUS', u"澳大利亚（Australia）"),
    ('ABW', u"阿鲁巴（Aruba）"),
    ('ALA', u"奥兰群岛（?aland Island）"),
    ('AZE', u"阿塞拜疆（Azerbaijan）"),
    ('BIH', u"波黑（Bosnia & Herzegovina）"),
    ('BRB', u"巴巴多斯（Barbados）"),
    ('BGD', u"孟加拉（Bangladesh）"),
    ('BEL', u"比利时（Belgium）"),
    ('BFA', u"布基纳法索（Burkina）"),
    ('BGR', u"保加利亚（Bulgaria）"),
    ('BHR', u"巴林（Bahrain）"),
    ('BDI', u"布隆迪（Burundi）"),
    ('BEN', u"贝宁（Benin）"),
    ('BLM', u"圣巴泰勒米岛（Saint Barthélemy）"),
    ('BMU', u"百慕大（Bermuda）"),
    ('BRN', u"文莱（Brunei）"),
    ('BOL', u"玻利维亚（Bolivia）"),
    ('BES', u"荷兰加勒比区（Caribbean Netherlands）"),
    ('BRA', u"巴西（Brazil）"),
    ('BHS', u"巴哈马（The Bahamas）"),
    ('BTN', u"不丹（Bhutan）"),
    ('BVT', u"布韦岛（Bouvet Island）"),
    ('BWA', u"博茨瓦纳（Botswana）"),
    ('BLR', u"白俄罗斯（Belarus）"),
    ('BLZ', u"伯利兹（Belize）"),
    ('CAN', u"加拿大（Canada）"),
    ('CCK', u"科科斯群岛（Cocos (Keeling) Islands）"),
    ('CAF', u"中非（Central African Republic）"),
    ('CHE', u"瑞士（Switzerland）"),
    ('CHL', u"智利（Chile）"),
    ('CMR', u"喀麦隆（Cameroon）"),
    ('COL', u"哥伦比亚（Colombia）"),
    ('CRI', u"哥斯达黎加（Costa Rica）"),
    ('CUB', u"古巴（Cuba）"),
    ('CPV', u"佛得角（Cape Verde）"),
    ('CXR', u"圣诞岛（Christmas Island）"),
    ('CYP', u"塞浦路斯（Cyprus）"),
    ('CZE', u"捷克（Czech Republic）"),
    ('DEU', u"德国（Germany）"),
    ('DJI', u"吉布提（Djibouti）"),
    ('DNK', u"丹麦（Denmark）"),
    ('DMA', u"多米尼克（Dominica）"),
    ('DOM', u"多米尼加（Dominican Republic）"),
    ('DZA', u"阿尔及利亚（Algeria）"),
    ('ECU', u"厄瓜多尔（Ecuador）"),
    ('EST', u"爱沙尼亚（Estonia）"),
    ('EGY', u"埃及（Egypt）"),
    ('ESH', u"西撒哈拉（Western Sahara）"),
    ('ERI', u"厄立特里亚（Eritrea）"),
    ('ESP', u"西班牙（Spain）"),
    ('FIN', u"芬兰（Finland）"),
    ('FJI', u"斐济群岛（Fiji）"),
    ('FLK', u"马尔维纳斯群岛（ 福克兰）（Falkland Islands）"),
    ('FSM', u"密克罗尼西亚联邦（Federated States of Micronesia）"),
    ('FRO', u"法罗群岛（Faroe Islands）"),
    ('FRA', u"法国（France）"),
    ('GAB', u"加蓬（Gabon）"),
    ('GRD', u"格林纳达（Grenada）"),
    ('GEO', u"格鲁吉亚（Georgia）"),
    ('GUF', u"法属圭亚那（French Guiana）"),
    ('GHA', u"加纳（Ghana）"),
    ('GIB', u"直布罗陀（Gibraltar）"),
    ('GRL', u"格陵兰（Greenland）"),
    ('GIN', u"几内亚（Guinea）"),
    ('GLP', u"瓜德罗普（Guadeloupe）"),
    ('GNQ', u"赤道几内亚（Equatorial Guinea）"),
    ('GRC', u"希腊（Greece）"),
    ('SGS', u"南乔治亚岛和南桑威奇群岛（South Georgia and the South Sandwich Islands）"),
    ('GTM', u"危地马拉（Guatemala）"),
    ('GUM', u"关岛（Guam）"),
    ('GNB', u"几内亚比绍（Guinea-Bissau）"),
    ('GUY', u"圭亚那（Guyana）"),
    ('HMD', u"赫德岛和麦克唐纳群岛（Heard Island and McDonald Islands）"),
    ('HND', u"洪都拉斯（Honduras）"),
    ('HRV', u"克罗地亚（Croatia）"),
    ('HTI', u"海地（Haiti）"),
    ('HUN', u"匈牙利（Hungary）"),
    ('IDN', u"印尼（Indonesia）"),
    ('IRL', u"爱尔兰（Ireland）"),
    ('ISR', u"以色列（Israel）"),
    ('IMN', u"马恩岛（Isle of Man）"),
    ('IND', u"印度（India）"),
    ('IOT', u"英属印度洋领地（British Indian Ocean Territory）"),
    ('IRQ', u"伊拉克（Iraq）"),
    ('IRN', u"伊朗（Iran）"),
    ('ISL', u"冰岛（Iceland）"),
    ('ITA', u"意大利（Italy）"),
    ('JEY', u"泽西岛（Jersey）"),
    ('JAM', u"牙买加（Jamaica）"),
    ('JOR', u"约旦（Jordan）"),
    ('JPN', u"日本（Japan）"),
    ('KHM', u"柬埔寨（Cambodia）"),
    ('KIR', u"基里巴斯（Kiribati）"),
    ('COM', u"科摩罗（The Comoros）"),
    ('KWT', u"科威特（Kuwait）"),
    ('CYM', u"开曼群岛（Cayman Islands）"),
    ('LBN', u"黎巴嫩（Lebanon）"),
    ('LIE', u"列支敦士登（Liechtenstein）"),
    ('LKA', u"斯里兰卡（Sri Lanka）"),
    ('LBR', u"利比里亚（Liberia）"),
    ('LSO', u"莱索托（Lesotho）"),
    ('LTU', u"立陶宛（Lithuania）"),
    ('LUX', u"卢森堡（Luxembourg）"),
    ('LVA', u"拉脱维亚（Latvia）"),
    ('LBY', u"利比亚（Libya）"),
    ('MAR', u"摩洛哥（Morocco）"),
    ('MCO', u"摩纳哥（Monaco）"),
    ('MDA', u"摩尔多瓦（Moldova）"),
    ('MNE', u"黑山（Montenegro）"),
    ('MAF', u"法属圣马丁（Saint Martin (France)）"),
    ('MDG', u"马达加斯加（Madagascar）"),
    ('MHL', u"马绍尔群岛（Marshall islands）"),
    ('MKD', u"马其顿（Republic of Macedonia (FYROM)）"),
    ('MLI', u"马里（Mali）"),
    ('MMR', u"缅甸（Myanmar (Burma)）"),
    ('MTQ', u"马提尼克（Martinique）"),
    ('MRT', u"毛里塔尼亚（Mauritania）"),
    ('MSR', u"蒙塞拉特岛（Montserrat）"),
    ('MLT', u"马耳他（Malta）"),
    ('MDV', u"马尔代夫（Maldives）"),
    ('MWI', u"马拉维（Malawi）"),
    ('MEX', u"墨西哥（Mexico）"),
    ('MYS', u"马来西亚（Malaysia）"),
    ('NAM', u"纳米比亚（Namibia）"),
    ('NER', u"尼日尔（Niger）"),
    ('NFK', u"诺福克岛（Norfolk Island）"),
    ('NGA', u"尼日利亚（Nigeria）"),
    ('NIC', u"尼加拉瓜（Nicaragua）"),
    ('NLD', u"荷兰（Netherlands）"),
    ('NOR', u"挪威（Norway）"),
    ('NPL', u"尼泊尔（Nepal）"),
    ('NRU', u"瑙鲁（Nauru）"),
    ('OMN', u"阿曼（Oman）"),
    ('PAN', u"巴拿马（Panama）"),
    ('PER', u"秘鲁（Peru）"),
    ('PYF', u"法属波利尼西亚（French polynesia）"),
    ('PNG', u"巴布亚新几内亚（Papua New Guinea）"),
    ('PHL', u"菲律宾（The Philippines）"),
    ('PAK', u"巴基斯坦（Pakistan）"),
    ('POL', u"波兰（Poland）"),
    ('PCN', u"皮特凯恩群岛（Pitcairn Islands）"),
    ('PRI', u"波多黎各（Puerto Rico）"),
    ('PSE', u"巴勒斯坦（Palestinian territories）"),
    ('PLW', u"帕劳（Palau）"),
    ('PRY', u"巴拉圭（Paraguay）"),
    ('QAT', u"卡塔尔（Qatar）"),
    ('REU', u"留尼汪（Réunion）"),
    ('ROU', u"罗马尼亚（Romania）"),
    ('SRB', u"塞尔维亚（Serbia）"),
    ('RUS', u"俄罗斯（Russian Federation）"),
    ('RWA', u"卢旺达（Rwanda）"),
    ('SLB', u"所罗门群岛（Solomon Islands）"),
    ('SYC', u"塞舌尔（Seychelles）"),
    ('SDN', u"苏丹（Sudan）"),
    ('SWE', u"瑞典（Sweden）"),
    ('SGP', u"新加坡（Singapore）"),
    ('SVN', u"斯洛文尼亚（Slovenia）"),
    ('SJM', u"斯瓦尔巴群岛和 扬马延岛（Template:Country data SJM Svalbard）"),
    ('SVK', u"斯洛伐克（Slovakia）"),
    ('SLE', u"塞拉利昂（Sierra Leone）"),
    ('SMR', u"圣马力诺（San Marino）"),
    ('SEN', u"塞内加尔（Senegal）"),
    ('SOM', u"索马里（Somalia）"),
    ('SUR', u"苏里南（Suriname）"),
    ('SSD', u"南苏丹（South Sudan）"),
    ('STP', u"圣多美和普林西比（Sao Tome & Principe）"),
    ('SLV', u"萨尔瓦多（El Salvador）"),
    ('SYR', u"叙利亚（Syria）"),
    ('SWZ', u"斯威士兰（Swaziland）"),
    ('TCA', u"特克斯和凯科斯群岛（Turks & Caicos Islands）"),
    ('TCD', u"乍得（Chad）"),
    ('TGO', u"多哥（Togo）"),
    ('THA', u"泰国（Thailand）"),
    ('TKL', u"托克劳（Tokelau）"),
    ('TLS', u"东帝汶（Timor-Leste (East Timor)）"),
    ('TUN', u"突尼斯（Tunisia）"),
    ('TON', u"汤加（Tonga）"),
    ('TUR', u"土耳其（Turkey）"),
    ('TUV', u"图瓦卢（Tuvalu）"),
    ('TZA', u"坦桑尼亚（Tanzania）"),
    ('UKR', u"乌克兰（Ukraine）"),
    ('UGA', u"乌干达（Uganda）"),
    ('USA', u"美国（United States of America (USA)）"),
    ('URY', u"乌拉圭（Uruguay）"),
    ('VAT', u"梵蒂冈（Vatican City (The Holy See)）"),
    ('VEN', u"委内瑞拉（Venezuela）"),
    ('VGB', u"英属维尔京群岛（British Virgin Islands）"),
    ('VIR', u"美属维尔京群岛（United States Virgin Islands）"),
    ('VNM', u"越南（Vietnam）"),
    ('WLF', u"瓦利斯和富图纳（Wallis and Futuna）"),
    ('WSM', u"萨摩亚（Samoa）"),
    ('YEM', u"也门（Yemen）"),
    ('MYT', u"马约特（Mayotte）"),
    ('ZAF', u"南非（South Africa）"),
    ('ZMB', u"赞比亚（Zambia）"),
    ('ZWE', u"津巴布韦（Zimbabwe）"),
    ('COG', u"刚果（布）（Republic of the Congo）"),
    ('COD', u"刚果（金）（Democratic Republic of the Congo）"),
    ('MOZ', u"莫桑比克（Mozambique）"),
    ('GGY', u"根西岛（Guernsey）"),
    ('GMB', u"冈比亚（Gambia）"),
    ('MNP', u"北马里亚纳群岛（Northern Mariana Islands）"),
    ('ETH', u"埃塞俄比亚（Ethiopia）"),
    ('NCL', u"新喀里多尼亚（New Caledonia）"),
    ('VUT', u"瓦努阿图（Vanuatu）"),
    ('ATF', u"法属南部领地（French Southern Territories）"),
    ('NIU', u"纽埃（Niue）"),
    ('UMI', u"美国本土外小岛屿（United States Minor Outlying Islands）"),
    ('COK', u"库克群岛（Cook Islands）"),
    ('GBR', u"英国（Great Britain (United Kingdom; England)）"),
    ('TTO', u"特立尼达和多巴哥（Trinidad & Tobago）"),
    ('VCT', u"圣文森特和格林纳丁斯（St. Vincent & the Grenadines）"),
    ('NZL', u"新西兰（New Zealand）"),
    ('SAU', u"沙特阿拉伯（Saudi Arabia）"),
    ('LAO', u"老挝（Laos）"),
    ('PRK', u"朝鲜（北朝鲜）（North Korea）"),
    ('KOR', u"韩国（南朝鲜）（South Korea）"),
    ('PRT', u"葡萄牙（Portugal）"),
    ('KGZ', u"吉尔吉斯斯坦（Kyrgyzstan）"),
    ('KAZ', u"哈萨克斯坦（Kazakhstan）"),
    ('TJK', u"塔吉克斯坦（Tajikistan）"),
    ('TKM', u"土库曼斯坦（Turkmenistan）"),
    ('UZB', u"乌兹别克斯坦（Uzbekistan）"),
    ('KNA', u"圣基茨和尼维斯（St. Kitts & Nevis）"),
    ('SPM', u"圣皮埃尔和密克隆（Saint-Pierre and Miquelon）"),
    ('SHN', u"圣赫勒拿（St. Helena & Dependencies）"),
    ('LCA', u"圣卢西亚（St. Lucia）"),
    ('MUS', u"毛里求斯（Mauritius）"),
    ('CIV', u"科特迪瓦（C?te d'Ivoire）"),
    ('KEN', u"肯尼亚（Kenya）"),
    ('MNG', u"蒙古国（Mongolia）"),
)

DOMAIN_TYPE = (
    (u"国家科技部领域", u"国家科技部领域"),
    (u"国家基金委领域", u"国家基金委领域"),
    (u"行业分类", u"行业分类"),
    (u"中图分类", u"中图分类"),
)

MINZU_CHOICE = (
    (u"汉族", u"汉族"),
    (u"壮族", u"壮族"),
    (u"满族", u"满族"),
    (u"回族", u"回族"),
    (u"苗族", u"苗族"),
    (u"维吾尔族", u"维吾尔族"),
    (u"土家族", u"土家族"),
    (u"彝族", u"彝族"),
    (u"蒙古族", u"蒙古族"),
    (u"藏族", u"藏族"),
    (u"布依族", u"布依族"),
    (u"侗族", u"侗族"),
    (u"瑶族", u"瑶族"),
    (u"朝鲜族", u"朝鲜族"),
    (u"白族", u"白族"),
    (u"哈尼族", u"哈尼族"),
    (u"哈萨克族", u"哈萨克族"),
    (u"黎族", u"黎族"),
    (u"傣族", u"傣族"),
    (u"畲族", u"畲族"),
    (u"傈僳族", u"傈僳族"),
    (u"仡佬族", u"仡佬族"),
    (u"东乡族", u"东乡族"),
    (u"高山族", u"高山族"),
    (u"拉祜族", u"拉祜族"),
    (u"水族", u"水族"),
    (u"佤族", u"佤族"),
    (u"纳西族", u"纳西族"),
    (u"羌族", u"羌族"),
    (u"土族", u"土族"),
    (u"仫佬族", u"仫佬族"),
    (u"锡伯族", u"锡伯族"),
    (u"柯尔克孜族", u"柯尔克孜族"),
    (u"达斡尔族", u"达斡尔族"),
    (u"景颇族", u"景颇族"),
    (u"毛南族", u"毛南族"),
    (u"撒拉族", u"撒拉族"),
    (u"布朗族", u"布朗族"),
    (u"塔吉克族", u"塔吉克族"),
    (u"阿昌族", u"阿昌族"),
    (u"普米族", u"普米族"),
    (u"鄂温克族", u"鄂温克族"),
    (u"怒族", u"怒族"),
    (u"京族", u"京族"),
    (u"基诺族", u"基诺族"),
    (u"德昂族", u"德昂族"),
    (u"保安族", u"保安族"),
    (u"俄罗斯族", u"俄罗斯族"),
    (u"裕固族", u"裕固族"),
    (u"乌孜别克族", u"乌孜别克族"),
    (u"门巴族", u"门巴族"),
    (u"鄂伦春族", u"鄂伦春族"),
    (u"独龙族", u"独龙族"),
    (u"塔塔尔族", u"塔塔尔族"),
    (u"赫哲族", u"赫哲族"),
    (u"珞巴族", u"珞巴族"),
)

XUELI_CHOICE = (
    (u"博士研究生", u"博士研究生"),
    (u"硕士研究生", u"硕士研究生"),
    (u"本科生", u"本科生"),
    (u"大专", u"大专"),
    (u"中专", u"中专"),
    (u"其他", u"其他"),
)

XUEWEI_CHOICE = (
    (u"博士", u"博士"),
    (u"硕士", u"硕士"),
    (u"学士", u"学士"),
    (u"其他", u"其他"),
)

ZHENGJIANLEIXING_CHOICE = {
    (u"身份证", u"身份证"),
    (u"其他", u"其他"),
}

BASE_DIR = 'upload'
PICTURE_BASE = 'pictures'
ATTACHMENT_BASE = 'attachments'
REVIEW_BASE = 'review'

def picture_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    if len(ext) > 4:
        ext = "jpg"
    filename = "picture.%s" % ext
    filepath = os.path.join(BASE_DIR, str(instance.id), PICTURE_BASE, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
    return filepath

def attachment_directory_path(instance, filename):
    return os.path.join(BASE_DIR, str(instance.expert.id), ATTACHMENT_BASE, filename)

def review_attachment_directory_path(instance, filename):
    return os.path.join(BASE_DIR, str(instance.project.id), REVIEW_BASE, str(instance.expert.id), filename)


# Step 1 ~ Step 7
class Expert(models.Model):
    USERNAME_FIELD = 'keystone_username'
    # 账号信息 -- Step 1
    expertname = models.CharField(max_length=32, verbose_name=u"*中文姓名", help_text=u"专家姓名", null=True, blank=True)
    keystone_uuid = models.CharField(max_length=64, verbose_name=u"UUID", help_text=u"账号UUID", null=True, blank=True)
    keystone_username = models.CharField(max_length=64, verbose_name=u"*用户名", help_text=u"专家账号用户名")
    keystone_initial_pwd = models.CharField(max_length=128, verbose_name=u"*初始密码", help_text=u"输入初始密码")
    email = models.EmailField(verbose_name=u"*邮箱", help_text=u"电子邮箱，例如：abc123@example.com")
    email_verified = models.BooleanField(default=False, verbose_name=u"邮箱地址是否已验证", help_text=u"是否已经验证邮箱地址")
    email_verified_words = models.CharField(max_length=128, verbose_name=u"邮箱验证秘钥", help_text=u"邮箱地址验证秘钥，用于验证邮箱是否有效", null=True)

    # 基本信息 -- Step 2
    picture = models.ImageField(verbose_name=u"*照片", upload_to=picture_directory_path, help_text=u"照片（小于1M）", null=True, blank=True)
    cengyong_name = models.CharField(max_length=32, verbose_name=u"曾用名", help_text=u"曾用名", null=True, blank=True)
    pinyin_name = models.CharField(max_length=32, verbose_name=u"拼音或英文名", help_text=u"拼音或英文名", null=True, blank=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICE, verbose_name=u"*性别", help_text=u"性别", null=True, blank=True)
    born = models.DateField(auto_now_add=False, verbose_name=u"*出生日期", help_text=u"出生日期，年月日", null=True, blank=True)
    chushengdi = models.CharField(max_length=32, verbose_name=u"出生地", help_text=u"出生地，例如：甘肃兰州", null=True, blank=True)
    guoji = models.CharField(max_length=32, choices=COUNTRY_CHOICE, verbose_name=u"*国籍", help_text=u"国籍，例如：中国", null=True, blank=True)
    jiguan = models.CharField(max_length=32, verbose_name=u"*籍贯", help_text=u"籍贯，例如：甘肃兰州", null=True, blank=True)
    minzu = models.CharField(max_length=32, choices=MINZU_CHOICE, verbose_name=u"*民族", help_text=u"民族，例如：汉族", null=True, blank=True)
    zhengzhimianmao = models.CharField(max_length=32, verbose_name=u"政治面貌", help_text=u"政治面貌，例如：党员", null=True, blank=True)
    zhengjianleixing = models.CharField(max_length=32, choices=ZHENGJIANLEIXING_CHOICE, verbose_name=u"*证件类型", help_text=u"证件类型：例如：身份证", null=True, blank=True)
    zhengjianhaoma = models.CharField(max_length=64, verbose_name=u"*证件号码", help_text=u"证件号码：允许数字、英文字母", null=True, blank=True)

    #银行账号信息 -- Step 3
    kaihuyinhang = models.CharField(max_length=32, verbose_name=u"*开户银行", help_text=u"开户银行，例如：中国银行", null=True, blank=True)
    kaihuhuming = models.CharField(max_length=64, verbose_name=u"*开户户名", help_text=u"户名，需与本人姓名一致", null=True, blank=True)
    kaihuzhanghao = models.CharField(max_length=64, verbose_name=u"*开户帐号", help_text=u"账号，允许数字", null=True, blank=True)
    suoshuzhihang = models.CharField(max_length=64, verbose_name=u"*所属支行", help_text=u"支行，例如：中国银行兰州市城关中心支行", null=True, blank=True)

    #所在单位信息 -- Step 4
    suozaidaiwei = models.CharField(max_length=64, verbose_name=u"所在单位", help_text=u"所在单位，括号请用半角括号", null=True, blank=True)
    danweixinzhi = models.CharField(max_length=64, verbose_name=u"*单位性质", help_text=u"单位性质：例如：事业单位", null=True, blank=True)
    suozaibumen = models.CharField(max_length=64, verbose_name=u"所在二级单位（部门）", help_text=u"所在二级单位（部门）信息", null=True, blank=True)
    danweisuozaisheng = models.CharField(max_length=32, verbose_name=u"*单位所在省", help_text=u"例如：甘肃省", null=True, blank=True)
    danweisuozaishi = models.CharField(max_length=32, verbose_name=u"*单位所在市", help_text=u"例如：兰州市", null=True, blank=True)
    tongxundizhi = models.CharField(max_length=256, verbose_name=u"*通讯地址", help_text=u"该地址用于接收函件", null=True, blank=True)
    youzhengbianma = models.CharField(max_length=32, verbose_name=u"邮政编码", help_text=u"邮编，例如：730030", null=True, blank=True)
    zhiwu = models.CharField(max_length=32, verbose_name=u"*职务", help_text=u"担任之职务", null=True, blank=True)
    zhiwujibie = models.CharField(max_length=32, verbose_name=u"职务级别", help_text=u"该职务所属的级别", null=True, blank=True)
    zhicheng = models.CharField(max_length=32, verbose_name=u"*职称", help_text=u"职称", null=True, blank=True)
    gongzuoxingzhi = models.CharField(max_length=64, verbose_name=u"*工作性质", help_text=u"工作性质，例如：全职", null=True, blank=True)

    #学历信息 -- Step 5
    zuigaoxueli = models.CharField(max_length=64, choices=XUELI_CHOICE, verbose_name=u"*最高学历", help_text=u"最高学历，例如：博士研究生", null=True, blank=True)
    zuigaoxuewei = models.CharField(max_length=64, choices=XUEWEI_CHOICE, verbose_name=u"*最高学位", help_text=u"最高学位，例如：博士学位", null=True, blank=True)
    xueweishouyudiqu = models.CharField(max_length=64, choices=COUNTRY_CHOICE, verbose_name=u"最高学位授予国或地区", help_text=u"授予最高学位的院校所在的国家或地区", null=True, blank=True)
    xueweishouyuriqi = models.CharField(max_length=32, verbose_name=u"最高学位授予年份", help_text=u"授予最高学位的年份，如：1997", null=True, blank=True)
    biyeyuanxiao = models.CharField(max_length=64, verbose_name=u"毕业院校", help_text=u"获取最高学历学位的毕业院校名称", null=True, blank=True)
    xueweishouyuyuanxiao = models.CharField(max_length=64, verbose_name=u"*获得最高学位院校", help_text=u"授予最高学位的院校名称", null=True, blank=True)
    suoxuezhuanye = models.CharField(max_length=64, verbose_name=u"*所学专业", help_text=u"所学专业的名称", null=True, blank=True)
    xianzhuanye = models.CharField(max_length=64, verbose_name=u"*现从事专业", help_text=u"现从事的专业名称", null=True, blank=True)
    isBodao = models.BooleanField(default=False, verbose_name=u"是否博士生导师", help_text=u"是否为博士生导师，默认为否")
    isLiangYuanYuanshi = models.BooleanField(default=False, verbose_name=u"*是否两院院士", help_text=u"是否为两院院士，默认为否")

    #其他 -- Step 6
    mobile = models.CharField(max_length=32, verbose_name=u"*移动电话", help_text=u"移动电话，请去除空格、保留国家码，例如：+8613912341234", null=True, blank=True)
    mobile_verified = models.BooleanField(default=False, verbose_name=u"手机号是否已验证", help_text=u"是否已经验证手机号码")
    workphone = models.CharField(max_length=32, verbose_name=u"*办公电话", help_text=u"办公室电话，请去除空格，保留国家、地区码，例如：+869311234567", null=True, blank=True)
    homephone = models.CharField(max_length=32, verbose_name=u"家庭电话", help_text=u"家庭电话，请去除空格，保留国家、地区码，例如：+869311234567", null=True, blank=True)
    fax = models.CharField(max_length=32, verbose_name=u"传真", help_text=u"传真号码，请去除空格，保留国家、地区码，例如：+869311234567", null=True, blank=True)
    personal_web = models.URLField(verbose_name=u"个人学术网址", help_text=u"个人学术网址，例如：http://abc.example.com", null=True, blank=True)
    weibo = models.CharField(max_length=64, verbose_name=u"微博", help_text=u"微博名或微博号或微博网址，例如：故宫博物院 或者：https://weibo.com/gugongweb", null=True, blank=True)
    jinjilianxiren = models.CharField(max_length=32, verbose_name=u"紧急联系人", help_text=u"紧急联系人姓名", null=True, blank=True)
    jinjilianxidianhua = models.CharField(max_length=32, verbose_name=u"紧急联系人电话", help_text=u"紧急联系人电话，允许手机或固定电话，请去除>空格、保留国家、地区码，例如：+8613912341234", null=True, blank=True)
    zhiyezizhi = models.CharField(max_length=64, verbose_name=u"职业资质", help_text=u"职业资质", null=True, blank=True)

    #学术专长或研究方向 -- Step 7
    zhuanchangfangxiang = models.TextField(max_length=4096, verbose_name=u"*学术专长或研究方向", help_text=u"学术专长或研究方向（限500字以内）", null=True, blank=True)

    #个人简介 -- Step 7
    gerenjianjie = models.TextField(max_length=4096, verbose_name=u"*个人简介", help_text=u"个人简历（限1000字）", null=True, blank=True)

    #享受特殊津贴、荣誉称号、其他需要特别说明事宜 -- Step 7
    teshujingtie = models.TextField(max_length=4096, verbose_name=u"享受特殊津贴", help_text=u"享受特殊津贴(限500字) ", null=True, blank=True)
    rongyuchenghao = models.TextField(max_length=4096, verbose_name=u"荣誉称号", help_text=u"荣誉称号（限500字）", null=True, blank=True)
    others = models.TextField(max_length=4096, verbose_name=u"其他需要特别说明事宜", help_text=u"其他需要特别说明事宜（限500字）", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)
    state = models.CharField(max_length=32, verbose_name=u"状态", help_text=u"状态")


#人才称号 -- Step 8
class ExpertTitle(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    rencaichenghao = models.CharField(max_length=64, choices=CHENGHAO_CHOICES, default=CHENGHAO_DEFAULT, verbose_name=u"人才称号", help_text=u"称号，多选", null=True, blank=True)


#专家类型 -- Step 9
class ExpertClass(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    zhuanjialeixing = models.CharField(max_length=32, choices=ZHUANJIALEIXING_CHOICES, verbose_name=u"*专家类型（多选）", help_text=u"专家类型（多选）", null=True, blank=True)

# DOMAIN = (
#     (u"国家科技部领域",(
#         (u"数学", u"数学"),
#         (u"信息科学与系统科学", u"信息科学与系统科学"),
#         (u"物理学", u"物理学"),
#         )
#      ),
#     (u"国家基金委领域", (
#         (u"数理科学", u"数理科学"),
#         (u"化学科学", u"化学科学"),
#         (u"生命科学", u"生命科学"),
#      )
# )

#DOMAIN = {
#     u"国家科技部领域": [u"数学",u"A001 数学一级",u"A0001 数学二级",u"A0002 数学二级",u"A002 数学一级",u"A0001 数学二级", u"信息科学与系统科学", u"物理学",],
#     u"国家基金委领域": [u"数理科学", u"化学科学", u"生命科学",],
# }
DOMAIN = {
"国家科技部领域": [u"110数学",u"11011数学史",u"11014数理逻辑与数学基础",u"11017数论",u"11021代数学",u"11024代数几何学",u"11027几何学",u"11031拓扑学",u"11034数学分析",u"11037非标准分析",u"11041函数论",u"11044常微分方程",u"11047偏微分方程",u"11051动力系统",u"11054积分方程",u"11057泛函分析",u"11061计算数学",u"11064概率论",u"11067数理统计学",u"11071应用统计数学",u"11074运筹学",u"11077组合数学",u"11081离散数学",u"11084模糊数学",u"11085计算机数学",u"11087应用数学",u"11099数学其他学科",u"120信息科学与系统科学",u"12010信息科学与系统科学基础学科",u"12020系统学",u"12030控制理论",u"12040系统评估与可行性分析",u"12050系统工程方法论",u"12099信息科学与系统科学其他学科",u"130力学",u"13010基础力学",u"13015固体力学",u"13020振动与波",u"13025流体力学",u"13030流变学",u"13035爆炸力学",u"13040物理力学",u"13041生物力学",u"13045统计力学",u"13050应用力学",u"13099力学其他学科",u"140物理学",u"14010物理学史",u"14015理论物理学",u"14020声学",u"14025热学",u"14030光学",u"14035电磁学",u"14040无线电物理",u"14045电子物理学",u"14050凝聚态物理学",u"14055等离子体物理学",u"14060原子分子物理学",u"14065原子核物理学",u"14070高能物理学",u"14075计算物理学",u"14080应用物理学",u"14099物理学其他学科",u"150化学",u"15010化学史",u"15015无机化学",u"15020有机化学",u"15025分析化学",u"15030物理化学",u"15035化学物理学",u"15040高分子物理",u"15045高分子化学",u"15050核化学",u"15055应用化学",u"15060化学生物学",u"15065材料化学",u"15099化学其他学科",u"160天文学",u"16010天文学史",u"16015天体力学",u"16020天体物理学",u"16025宇宙化学",u"16030天体测量学",u"16035射电天文学",u"16040空间天文学",u"16045天体演化学",u"16050星系与宇宙学",u"16055恒星与银河系",u"16060太阳与太阳系",u"16065天体生物学",u"16070天文地球动力学",u"16075时间测量学",u"16099天文学其他学科",u"170地球科学",u"17010地球科学史",u"17015大气科学",u"17020固体地球物理学",u"17025空间物理学",u"17030地球化学",u"17035大地测量学",u"17040地图学",u"17045地理学",u"17050地质学",u"17055水文学",u"17060海洋科学",u"17099地球科学其他学科",u"180生物学",u"18011生物数学",u"18014生物物理学",u"18017生物化学",u"18021细胞生物学",u"18022免疫学",u"18024生理学",u"18027发育生物学",u"18031遗传学",u"18034放射生物学",u"18037分子生物学",u"18039专题生物学研究",u"18041生物进化论",u"18044生态学",u"18047神经生物学",u"18051植物学",u"18054昆虫学",u"18057动物学",u"18061微生物学",u"18064病毒学",u"18067人类学",u"18099生物学其他学科",u"190心理学",u"19010心理学史",u"19015认知心理学",u"19020社会心理学",u"19025实验心理学",u"19030发展心理学",u"19040医学心理学",u"19041人格心理学",u"19042临床与咨询心理学",u"19045心理测量",u"19046心理统计",u"19050生理心理学",u"19055工业心理学",u"19060管理心理学",u"19065应用心理学",u"19070教育心理学",u"19075法制心理学",u"19099心理学其他学科",u"210农学",u"21010农业史",u"21020农业基础学科",u"21030农艺学",u"21040园艺学",u"21045农产品贮藏与加工",u"21050土壤学",u"21060植物保护学",u"21099农学其他学科",u"220林学",u"22010林业基础学科",u"22015林木遗传育种学",u"22020森林培育学",u"22025森林经理学",u"22030森林保护学",u"22035野生动物保护与管理",u"22040防护林学",u"22045经济林学",u"22050园林学",u"22055林业工程",u"22060森林统计学",u"22065林业经济学",u"22099林学其他学科",u"230畜牧、兽医科学",u"23010畜牧、兽医科学基础学科",u"23020畜牧学",u"23030兽医学",u"23099畜牧、兽医科学其他学科",u"240水产学",u"24010水产学基础学科",u"24015水产增殖学",u"24020水产养殖学",u"24025水产饲料学",u"24030水产保护学",u"24035捕捞学",u"24040水产品贮藏与加工",u"24045水产工程学",u"24050水产资源学",u"24055水产经济学",u"24099水产学其他学科",u"310基础医学",u"31010医学史",u"31011医学生物化学",u"31014人体解剖学",u"31017医学细胞生物学",u"31021人体生理学",u"31024人体组织胚胎学",u"31027医学遗传学",u"31031放射医学",u"31034人体免疫学",u"31037医学寄生虫学",u"31041医学微生物学",u"31044病理学",u"31047药理学",u"31051医学实验动物学",u"31057医学统计学",u"31099基础医学其他学科",u"320临床医学",u"32011临床诊断学",u"32014保健医学",u"32017理疗学",u"32021麻醉学",u"32024内科学",u"32027外科学",u"32031妇产科学",u"32034儿科学",u"32037眼科学",u"32041耳鼻咽喉科学",u"32044口腔医学",u"32047皮肤病学",u"32051性医学",u"32054神经病学",u"32057精神病学",u"32058重症医学",u"32061急诊医学",u"32064核医学",u"32065全科医学",u"32067肿瘤学",u"32071护理学",u"32099临床医学其他学科",u"330预防医学与公共卫生学",u"33011营养学",u"33014毒理学",u"33017消毒学",u"33021流行病学",u"33027媒介生物控制学",u"33031环境医学",u"33034职业病学",u"33037地方病学",u"33035热带医学",u"33041社会医学",u"33044卫生检验学",u"33047食品卫生学",u"33051儿少与学校卫生学",u"33054妇幼卫生学",u"33057环境卫生学",u"33061劳动卫生学",u"33064放射卫生学",u"33067卫生工程学",u"33071卫生经济学",u"33072卫生统计学",u"33074优生学",u"33077健康促进与健康教育学",u"33081卫生管理学",u"33099预防医学与公共卫生学其他学科",u"340军事医学与特种医学",u"34010军事医学",u"34020特种医学",u"34099军事医学与特种医学其他学科",u"350药学",u"35010药物化学",u"35020生物药物学",u"35025微生物药物学",u"35030放射性药物学",u"35035药剂学",u"35040药效学",u"35045药物管理学",u"35050药物统计学",u"35099药学其他学科",u"360中医学与中药学",u"36010中医学",u"36020民族医学",u"36030中西医结合医学",u"36040中药学",u"36099中医学与中药学其他学科",u"410工程与技术科学基础学科",u"41010工程数学",u"41015工程控制论",u"41020工程力学",u"41025工程物理学",u"41030工程地质学",u"41035工程水文学",u"41040工程仿生学",u"41045工程心理学",u"41050标准科学技术",u"41055计量学",u"41060工程图学",u"41065勘查技术",u"41070工程通用技术",u"41075工业工程学",u"41099工程与技术科学基础学科其他学科",u"413信息与系统科学相关工程与技术",u"41310控制科学与技术",u"41315仿真科学技术",u"41320信息安全技术",u"41330信息技术系统性应用",u"41399信息与系统科学相关工程与技术其他学科",u"416自然科学相关工程与技术",u"41610物理学相关工程与技术",u"41620光学工程",u"41630海洋工程与技术",u"41640生物工程",u"41650农业工程",u"41660生物医学工程学",u"420测绘科学技术",u"42010大地测量技术",u"42020摄影测量与遥感技术",u"42030地图制图技术",u"42040工程测量技术",u"42050海洋测绘",u"42060测绘仪器",u"42099测绘科学技术其他学科",u"430材料科学",u"43010材料科学基础学科",u"43015材料表面与界面",u"43020材料失效与保护",u"43025材料检测与分析技术",u"43030材料实验",u"43035材料合成与加工工艺",u"43040金属材料",u"43045无机非金属材料",u"43050有机高分子材料",u"43055复合材料",u"43060生物材料",u"43070纳米材料",u"43099材料科学其他学科",u"440矿山工程技术",u"44010矿山地质学",u"44015矿山测量",u"44020矿山设计",u"44025矿山地面工程",u"44030井巷工程",u"44035采矿工程",u"44040选矿工程",u"44045钻井工程",u"44050油气田井开发工程",u"44055石油、天然气储存与运输工程",u"44060矿山机械工程",u"44065矿山电气工程",u"44070采矿环境工程",u"44075矿山安全",u"44080矿山综合利用工程",u"44099矿山工程技术其他学科",u"450冶金工程技术",u"45010冶金物理化学",u"45015冶金反应工程",u"45020冶金原料与预处理",u"45025冶金热能工程",u"45030冶金技术",u"45035钢铁冶金",u"45040有色金属冶金",u"45045轧制",u"45050冶金机械及自动化",u"45099冶金工程技术其他学科",u"460机械工程",u"46010机械史",u"46015机械学",u"46020机械设计",u"46025机械制造工艺与设备",u"46030刀具技术",u"46035机床技术",u"46045流体传动与控制",u"46050机械制造自动化",u"46099机械工程其他学科",u"470动力与电气工程",u"47010工程热物理",u"47020热工学",u"47030动力机械工程",u"47035制冷与低温工程",u"47040电气工程",u"47099动力与电气工程其他学科",u"480能源科学技术",u"48010能源化学",u"48020能源地理学",u"48030能源计算与测量",u"48040储能技术",u"48050节能技术",u"48060一次能源",u"48070二次能源",u"48080能源系统工程",u"48099能源科学技术其他学科",u"490核科学技术",u"49010辐射物理与技术",u"49015核探测技术与核电子学",u"49020放射性计量学",u"49025核仪器、仪表",u"49030核材料与工艺技术",u"49035粒子加速器",u"49040裂变堆工程技术",u"49045核聚变工程技术",u"49050核动力工程技术",u"49055同位素技术",u"49060核爆炸工程",u"49065核安全",u"49070乏燃料后处理技术",u"49075辐射防护技术",u"49080核设施退役技术",u"49085放射性三废处理、处置技术",u"49099核科学技术其他学科",u"510电子与通信技术",u"51010电子技术",u"51020光电子学与激光技术",u"51030半导体技术",u"51040信息处理技术",u"51050通信技术",u"51060广播与电视工程技术",u"51070雷达工程",u"51099电子与通信技术其他学科",u"520计算机科学技术",u"52010计算机科学技术基础学科",u"52020人工智能",u"52030计算机系统结构",u"52040计算机软件",u"52050计算机工程",u"52060计算机应用",u"52099计算机科学技术其他学科",u"530化学工程",u"53011化学工程基础学科",u"53014化工测量技术与仪器仪表",u"53017化工传递过程",u"53021化学分离工程",u"53024化学反应工程",u"53027化工系统工程",u"53031化工机械与设备",u"53034无机化学工程",u"53037有机化学工程",u"53041电化学工程",u"53044高聚物工程",u"53047煤化学工程",u"53051石油化学工程",u"53052天然气化学工程",u"53054精细化学工程",u"53057造纸技术",u"53061毛皮与制革工程",u"53064制药工程",u"53067生物化学工程",u"53099化学工程其他学科",u"535产品应用相关工程与技术",u"53510仪器仪表技术",u"53520兵器科学与技术",u"53530产品应用专用性技术",u"53599产品应用相关工程与技术其他学科",u"540纺织科学技术",u"54010纺织科学技术基础学科",u"54020纺织材料",u"54030纤维制造技术",u"54040纺织技术",u"54050染整技术",u"54060服装技术",u"54070纺织机械与设备",u"54099纺织科学技术其他学科",u"550食品科学技术",u"55010食品科学技术基础学科",u"55020食品加工技术",u"55030食品包装与储藏",u"55040食品机械",u"55050食品加工的副产品加工与利用",u"55060食品工业企业管理学",u"55070食品工程与粮油工程",u"55099食品科学技术其他学科",u"560土木建筑工程",u"56010建筑史",u"56015土木建筑工程基础学科",u"56020土木建筑工程测量",u"56025建筑材料",u"56030工程结构",u"56035土木建筑结构",u"56040土木建筑工程设计",u"56045土木建筑工程施工",u"56050土木工程机械与设备",u"56055市政工程",u"56060建筑经济学",u"56099土木建筑工程其他学科",u"570水利工程",u"57010水利工程基础学科",u"57015水利工程测量",u"57020水工材料",u"57025水工结构",u"57030水力机械",u"57035水利工程施工",u"57040水处理",u"57045河流泥沙工程学",u"57055环境水利",u"57060水利管理",u"57065防洪工程",u"57070水利经济学",u"57099水利工程其他学科",u"580交通运输工程",u"58010道路工程",u"58020公路运输",u"58030铁路运输",u"58040水路运输",u"58050船舶、舰船工程",u"58060航空运输",u"58070交通运输系统工程",u"58080交通运输安全工程",u"58099交通运输工程其他学科",u"590航空、航天科学技术",u"59010航空、航天科学技术基础学科",u"59015航空器结构与设计",u"59020航天器结构与设计",u"59025航空、航天推进系统",u"59030飞行器仪表、设备",u"59035飞行器控制、导航技术",u"59040航空、航天材料",u"59045飞行器制造技术",u"59050飞行器试验技术",u"59055飞行器发射与回收、飞行技术",u"59060航空航天地面设施、技术保障",u"59065航空、航天系统工程",u"59099航空、航天科学技术其他学科",u"610环境科学技术及资源科学技术",u"61010环境科学技术基础学科",u"61020环境学",u"61030环境工程学",u"61050资源科学技术",u"61099环境科学技术及资源科学技术其他学科",u"620安全科学技术",u"62010安全科学技术基础学科",u"62021安全社会科学",u"62023安全物质学",u"62025安全人体学",u"62027安全系统学",u"62030安全工程技术科学",u"62040安全卫生工程技术",u"62060安全社会工程",u"62070部门安全工程理论",u"62080公共安全",u"62099安全科学技术其他学科",u"630管理学",u"63010管理思想史",u"63015管理理论",u"63025管理计量学",u"63030部门经济管理",u"63032 区域经济管理",u"63035科学学与科技管理",u"63040企业管理",u"63044公共管理",u"63050管理工程",u"63055人力资源开发与管理",u"63060未来学",u"63099管理学其他学科",u"710马克思主义",u"71010马、恩、列、斯思想研究",u"71020毛泽东思想研究",u"71030马克思主义思想史",u"71040科学社会主义",u"71050社会主义运动史",u"71060国外马克思主义研究",u"71099马克思主义其他学科",u"720哲学",u"72010马克思主义哲学",u"72015自然辩证法",u"72020中国哲学史",u"72025东方哲学史",u"72030西方哲学史",u"72035现代外国哲学",u"72040逻辑学",u"72045伦理学",u"72050美学",u"72099哲学其他学科",u"730宗教学",u"73011宗教学理论",u"73014无神论",u"73017原始宗教",u"73021古代宗教",u"73024佛教",u"73027基督教",u"73031伊斯兰教",u"73034道教",u"73037印度教",u"73041犹太教",u"73044袄教",u"73047摩尼教",u"73051锡克教",u"73054耆那教",u"73057神道教",u"73061中国民间宗教与民间信仰",u"73064中国少数民族宗教",u"73067当代宗教",u"73099宗教学其他学科",u"740语言学",u"74010普通语言学",u"74015比较语言学",u"74020语言地理学",u"74025社会语言学",u"74030心理语言学",u"74035应用语言学",u"74040汉语研究",u"74045中国少数民族语言文字",u"74050外国语言",u"74099语言学其他学科",u"750文学",u"75011文学理论",u"75014文艺美学",u"75017文学批评",u"75021比较文学",u"75024中国古代文学",u"75027中国近代文学",u"75031中国现代文学",u"75034中国各体文学",u"75037中国民间文学",u"75041中国儿童文学",u"75044中国少数民族文学",u"75047世界文学史",u"75051东方文学",u"75054俄国文学",u"75057英国文学",u"75061法国文学",u"75064德国文学",u"75067意大利文学",u"75071美国文学",u"75074北欧文学",u"75077东欧文学",u"75081拉美文学",u"75084非洲文学",u"75087大洋洲文学",u"75099文学其他学科",u"760艺术学",u"76010艺术心理学",u"76015音乐",u"76020戏剧",u"76025戏曲",u"76030舞蹈",u"76035电影",u"76040广播电视文艺",u"76045美术",u"76050工艺美术",u"76055书法",u"76060摄影",u"76099艺术学其他学科",u"770历史学",u"77010史学史",u"77015史学理论",u"77020历史文献学",u"77025中国通史",u"77030中国古代史",u"77035中国近代史、现代史",u"77040世界通史",u"77045亚洲史",u"77050非洲史",u"77055美洲史",u"77060欧洲史",u"77065澳洲、大洋洲史",u"77070专门史",u"77099历史学其他学科",u"780考古学",u"78010考古理论",u"78020考古学史",u"78030考古技术",u"78040中国考古",u"78050外国考古",u"78060专门考古",u"78099考古学其他学科",u"790经济学",u"79011政治经济学",u"79013宏观经济学",u"79015微观经济学",u"79017比较经济学",u"79019经济地理学",u"79021发展经济学",u"79023生产力经济学",u"79025经济思想史",u"79027经济史",u"79029世界经济学",u"79031国民经济学",u"79033管理经济学",u"79035数量经济学",u"79037会计学",u"79039审计学",u"79041技术经济学",u"79043生态经济学",u"79045劳动经济学",u"79047城市经济学",u"79049资源经济学",u"79051环境经济学",u"79052可持续发展经济学",u"79053物流经济学",u"79055工业经济学",u"79057农村经济学",u"79059农业经济学",u"79061交通运输经济学",u"79063商业经济学",u"79065价格学",u"79067旅游经济学",u"79069信息经济学",u"79071财政学",u"79073金融学",u"79075保险学",u"79077国防经济学",u"79099经济学其他学科",u"810政治学",u"81010政治学理论",u"81020政治制度",u"81030行政学",u"81040国际政治学",u"81099政治学其他学科",u"820法学",u"82010理论法学",u"82020法律史学",u"82030部门法学",u"82040国际法学",u"82099法学其他学科",u"830军事学",u"83010军事理论",u"83015军事史",u"83020军事心理学",u"83025战略学",u"83030战役学",u"83035战术学",u"83040军队指挥学",u"83045军制学",u"83050军队政治工作学",u"83055军事后勤学",u"83060军事地学",u"83065军事技术",u"83099军事学其他学科",u"840社会学",u"84011社会学史",u"84014社会学理论",u"84017社会学方法",u"84021实验社会学",u"84024数理社会学",u"84027应用社会学",u"84031比较社会学",u"84034社会地理学",u"84037文化社会学",u"84041历史社会学",u"84044经济社会学",u"84047军事社会学",u"84054公共关系学",u"84057社会人类学",u"84061组织社会学",u"84064发展社会学",u"84067福利社会学",u"84071人口学",u"84074劳动科学",u"84099社会学其他学科",u"850民族学与文化学",u"85010民族问题理论",u"85020民族史学",u"85030蒙古学",u"85040藏学",u"85042新疆民族研究",u"85050文化人类学与民俗学",u"85060世界民族研究",u"85070文化学",u"85099民族和文化学其他学科",u"860新闻学与传播学",u"86010新闻理论",u"86020新闻史",u"86030新闻业务",u"86040新闻事业经营管理",u"86050广播与电视",u"86060传播学",u"86099新闻学与传播学其他学科",u"870图书馆、情报与文献学",u"87010图书馆学",u"87020文献学",u"87030情报学",u"87040档案学",u"87050博物馆学",u"87099图书馆、情报与文献学其他学科",u"880教育学",u"88011教育史",u"88014教育学原理",u"88017教学论",u"88021德育原理",u"88024教育社会学",u"88031教育经济学",u"88034教育管理学",u"88037比较教育学",u"88041教育技术学",u"88044军事教育学",u"88047学前教育学",u"88051普通教育学",u"88054高等教育学",u"88057成人教育学",u"88061职业技术教育学",u"88064特殊教育学",u"88099教育学其他学科",u"890体育科学",u"89010体育史",u"89015体育理论",u"89020运动生物力学",u"89025运动生理学",u"89030运动心理学",u"89035运动生物化学",u"89040体育保健学",u"89045运动训练学",u"89050体育教育学",u"89055武术理论与方法",u"89060体育管理学",u"89065体育经济学",u"89099体育科学其他学科",u"910统计学",u"91010统计学史",u"91030经济统计学",u"91035科学技术统计学",u"91040社会统计学",u"91045人口统计学",u"91050环境与生态统计学",u"91060生物与医学统计学",u"91099统计学其他学科"],
u"国家基金委领域": [u"国家自然科学基金学科分类",u"A数理科学部",u"A01数学",u"A0101数论",u"A010101解析数论",u"A010102代数数论",u"A010103数论应用",u"A0102代数学",u"A010201群及其表示",u"A010202李群与李代数",u"A010203代数群与量子群",u"A010204同调与K理论",u"A010205环与代数",u"A010206编码与密码",u"A010207代数几何",u"A0103几何学",u"A010301整体微分几何",u"A010302复几何与代数几何",u"A010303几何分析",u"A0104拓扑学",u"A010401代数拓扑与微分拓扑",u"A010402低维流形上的拓扑",u"A010403一般拓扑学",u"A0105函数论",u"A010501多复变函数论",u"A010502复动力系统",u"A010503单复变函数论",u"A010504调和分析与小波分析",u"A010505函数逼近论",u"A0106泛函分析",u"A010601非线性泛函分析",u"A010602算子理论与算子代数",u"A010603空间理论",u"A0107常微分方程与动力系统",u"A010701泛函微分方程",u"A010702定性理论与稳定性理论",u"A010703分支理论与混沌",u"A010704微分动力系统与哈密顿系统",u"A010705拓扑动力系统与遍历论",u"A0108偏微分方程",u"A010801几何、物理和力学中的偏微分方程",u"A010802非线性椭圆和非线性抛物方程",u"A010803混合型、退化型偏微分方程",u"A010804非线性发展方程和无穷维动力系统",u"A0109数学物理",u"A010901规范场论与超弦理论",u"A010902可积系统及其应用",u"A0110概率论与随机分析",u"A011001马氏过程与遍历论",u"A011002随机分析与随机过程",u"A011003随机微分方程",u"A011004极限理论",u"A0111数理统计",u"A011101抽样调查与试验设计",u"A011102时间序列与多元分析",u"A011103数据分析与统计计算",u"A0112运筹学",u"A011201线性与非线性规划",u"A011202组合最优化",u"A011203随机最优化",u"A011204可靠性理论",u"A0113控制论中的数学方法",u"A011301分布参数系统的控制理论",u"A011302随机系统的控制理论",u"A0114应用数学方法",u"A011401信息论",u"A011402经济数学与金融数学",u"A011403生物数学",u"A011404不确定性的数学理论",u"A011405分形论及应用",u"A0115数理逻辑和与计算机相关的数学",u"A011501数理逻辑",u"A011502公理集合论",u"A011503计算复杂性与符号计算",u"A011504机器证明",u"A0116组合数学",u"A011601组合设计",u"A011602图论",u"A011603代数组合与组合矩阵论",u"A0117计算数学与科学工程计算",u"A011701偏微分方程数值计算",u"A011702流体力学中的数值计算",u"A011703一般反问题的计算方法",u"A011704常微分方程数值计算",u"A011705数值代数",u"A011706数值逼近与计算几何",u"A011707谱方法及高精度数值方法",u"A011708有限元和边界元方法",u"A011709多重网格技术及区域分解",u"A011710自适应方法",u"A011711并行算法",u"A02力学",u"A0201力学中的基本问题和方法",u"A020101理性力学与力学中的数学方法",u"A020102物理力学",u"A020103力学中的反问题",u"A0202动力学与控制",u"A020201分析力学",u"A020202动力系统的分岔与混沌",u"A020203运动稳定性及其控制",u"A020204非线性振动及其控制",u"A020205多体系统动力学",u"A020206转子动力学",u"A020207弹道力学与飞行力学",u"A020208载运工具动力学及其控制",u"A020209多场耦合与智能结构动力学",u"A0203固体力学",u"A020301弹性力学与塑性力学",u"A020302损伤与断裂力学",u"A020303疲劳与可靠性",u"A020304本构关系",u"A020305复合材料力学",u"A020306智能材料与结构力学",u"A020307超常环境下材料和结构的力学行为",u"A020308微纳米力学",u"A020309接触、摩擦与磨损力学",u"A020310表面、界面与薄膜力学",u"A020311岩体力学和土力学",u"A020312结构力学与结构优化",u"A020313结构振动、噪声与控制",u"A020314流固耦合力学",u"A020315制造工艺力学",u"A020316实验固体力学",u"A020317计算固体力学",u"A0204流体力学",u"A020401湍流与流动稳定性",u"A020402水动力学",u"A020403空气动力学",u"A020404非平衡流与稀薄气体流动",u"A020405多相流与渗流",u"A020406非牛顿流与流变学",u"A020407流动噪声与气动声学",u"A020408流动控制和优化",u"A020409环境流体力学",u"A020410工业流体力学",u"A020411微重力流体力学",u"A020412交通流与颗粒流",u"A020413电磁与多场耦合流体力学",u"A020414实验流体力学",u"A020415计算流体力学",u"A0205生物力学",u"A020501组织与器官系统力学",u"A020502细胞、亚细胞、生物大分子力学",u"A020503仿生、生物材料与运动生物力学",u"A0206爆炸与冲击动力学",u"A020601爆炸力学",u"A020602冲击动力学",u"A03天文学",u"A0301宇宙学",u"A030101宇宙学模型和参数、早期宇宙",u"A030102宇宙结构的形成和演化及观测宇宙学",u"A030103宇宙暗物质和暗能量",u"A0302星系和类星体",u"A030201银河系",u"A030202星系形成、结构和演化",u"A030203星系相互作用和并合；活动星系核",u"A0303恒星与星际物质",u"A030301恒星结构和演化与恒星大气",u"A030302变星和激变变星、双星和多星系统",u"A030303恒星形成与早期演化、星际介质和星际分子",u"A030304晚期演化和致密天体及其相关高能过程",u"A030305太阳系外行星系统",u"A0304太阳和太阳系",u"A030401太阳磁场和太阳发电机",u"A030402太阳日冕物质抛射、耀斑、日珥和其他活动",u"A030403日震学和太阳内部结构；太阳黑子和太阳活动周期变化",u"A030404太阳系的起源和演化及太阳系中行星、卫星和其他小天体",u"A030405太阳爆发活动对日地空间天气的影响",u"A0305天体中基本物理过程的理论和实验",u"A030501天文中基本物理过程和天体辐射过程的理论和实验",u"A030502实验室天体物理",u"A0306天体测量和天文地球动力学",u"A030601天文参考系及星表",u"A030602相对论天体测量",u"A030603天文地球动力学及天体测量学的应用",u"A030604时间与频率",u"A0307天体力学和人造卫星动力学",u"A030701人造天体、太阳系小天体、行星系统和恒星系统动力学",u"A030702N体问题、非线性和相对论天体力学",u"A0308天文技术和方法",u"A030801光学、紫外和红外天文技术与方法",u"A030802射电、毫米波和亚毫米波天文技术与方法",u"A030803高能天体物理技术方法和空间天文技术与方法",u"A030804海量数据处理及数值模拟天文技术与方法",u"A0309中、西方天文学史",u"A0310天文学同其他学科的交叉",u"A04物理学I",u"A0401凝聚态物性I:结构、力学和热学性质",u"A040101固体结构和人工微结构",u"A040102软物质和液体的结构与性质",u"A040103凝聚态物质的力学、热学性质，相变和晶格动力学",u"A040104凝聚态物质的（非电子）输运性质",u"A040105薄膜和纳米结构的形成",u"A040106表面，薄膜和纳米结构的表征和分析",u"A040107表面、界面、介观系统、纳米系统的非电子性质",u"A0402凝聚态物性II：电子结构、电学、磁学和光学性质",u"A040201块体材料的电子态",u"A040202强关联电子系统",u"A040203电子输运过程：电导、光电导、磁电导",u"A040204表面、界面和低维系统的电子结构及电学性质",u"A040205介观系统和人工微结构的电子结构、光学和电学性质",u"A040206超导电性",u"A040207磁有序系统",u"A040208低维、介观和人工微结构的磁性",u"A040209介电、压电、热电和铁电性质",u"A040210凝聚态物质的光学和波谱学、物质与粒子的相互作用和辐射",u"A040211极端条件下的凝聚态物理",u"A040212量子计算中的凝聚态物理问题",u"A040213软物质、有机和生物材料的电子结构和物理",u"A040214生命现象中的凝聚态物理问题",u"A040215凝聚态物理中的新效应及其他问题",u"A0403原子和分子物理",u"A040301原子和分子结构理论",u"A040302原子、分子、光子相互作用与光谱",u"A040303原子分子碰撞过程及相互作用",u"A040304大分子、团簇与特殊原子分子性质",u"A040305极端条件下的原子分子物理",u"A040306外场中的原子分子性质及其操控",u"A040307量子信息中的原子分子物理问题",u"A040308与原子、分子有关的其他物理问题",u"A0404光学",u"A040401光的传播和成像",u"A040402信息光学中的物理问题",u"A040403光源、光学器件和光学系统中的物理问题",u"A040404纤维光学和集成光学中的物理问题",u"A040405光与物质的相互作用",u"A040406超强、超快光物理",u"A040407微纳光学与光子学",u"A040408量子光学和量子信息",u"A040409非线性光学",u"A040410光学材料中物理问题及固体发光",u"A040411激光光谱学及高分辨高灵敏光谱方法",u"A040412X-射线、红外、THz物理",u"A040413光学在生命科学中的应用",u"A040414与光学有关的其他物理问题和交叉学科",u"A0405声学",u"A040501线性与非线性声学",u"A040502水声和海洋声学及空气动力声学",u"A040503超声学、量子声学和声学效应",u"A040504噪声、噪声效应及其控制",u"A040505生理、心理声学和生物声学",u"A040506语言声学、乐声及声学信号处理",u"A040507声学换能器、声学测量方法和声学材料",u"A040508信息科学中的声学问题",u"A040509建筑声学与电声学",u"A040510与声学有关的其他物理问题和交叉学科",u"A05物理学II",u"A0501基础物理学",u"A050101物理学中的数学问题与计算方法",u"A050102经典物理及其唯象学研究",u"A050103量子物理及其应用",u"A050104量子信息学",u"A050105统计物理学与复杂系统",u"A050106相对论、引力与宇宙学",u"A0502粒子物理学和场论",u"A050201场和粒子的一般理论及方法",u"A050202量子色动力学、强相互作用和强子物理",u"A050203电－弱相互作用及其唯象学",u"A050204非标准模型及其唯象学",u"A050205弦论、膜论及隐藏的空间维度",u"A050206非加速器粒子物理",u"A050207粒子天体物理和宇宙学",u"A0503核物理",u"A050301原子核结构与特性研究",u"A050302原子核高激发态、高自旋态和超形变",u"A050303核裂变、核聚变、核衰变",u"A050304重离子核物理",u"A050305放射性核束物理、超重元素合成及反应机制",u"A050306中高能核物理",u"A050307核天体物理",u"A0504核技术及其应用",u"A050401离子束与物质相互作用和辐照损伤",u"A050402离子束核分析技术",u"A050403核效应分析技术",u"A050404中子技术及其应用",u"A050405加速器质谱技术",u"A050406离子注入及离子束材料改性",u"A050407核技术在环境科学、地学和考古中的应用",u"A050408核技术在工、农业和医学中的应用",u"A050409新概念、新原理、新方法",u"A0505粒子物理与核物理实验方法与技术",u"A050501束流物理与加速器技术",u"A050502荷电粒子源、靶站和预加速装置",u"A050503束流传输和测量技术",u"A050504反应堆物理与技术",u"A050505散裂中子源相关技术",u"A050506探测技术和谱仪",u"A050507辐射剂量学和辐射防护",u"A050508实验数据获取与处理",u"A050509新原理、新方法、新技术、新应用",u"A0506等离子体物理",u"A050601等离子体中的基本过程与特性",u"A050602等离子体产生、加热与约束",u"A050603等离子体中的波与不稳定性",u"A050604等离子体中的非线性现象",u"A050605等离子体与物质相互作用",u"A050606等离子体诊断",u"A050607强粒子束与辐射源",u"A050608磁约束等离子体",u"A050609惯性约束等离子体",u"A050610低温等离子体及其应用",u"A050611空间和天体等离子体及特殊等离子体",u"A0507同步辐射技术及其应用",u"A050701同步辐射光源原理和技术",u"A050702自由电子激光原理和技术",u"A050703束线光学技术和实验方法",u"B化学科学部",u"B01无机化学",u"B0101无机合成和制备化学",u"B010101合成与制备技术",u"B010102合成化学",u"B0102元素化学",u"B010201稀土化学",u"B010202主族元素化学",u"B010203过渡金属化学",u"B010204丰产元素与多酸化学",u"B0103配位化学",u"B010301固体配位化学",u"B010302溶液配位化学",u"B010303功能配合物化学",u"B0104生物无机化学",u"B010401金属蛋白（酶）化学",u"B010402生物微量元素化学",u"B010403细胞生物无机化学",u"B010404生物矿化及生物界面化学",u"B0105固体无机化学",u"B010501缺陷化学",u"B010502固相反应化学",u"B010503固体表面与界面化学",u"B010504固体结构化学",u"B0106物理无机化学",u"B010601无机化合物结构与性质",u"B010602理论无机化学",u"B010603无机光化学",u"B010604分子磁体",u"B010605无机反应热力学与动力学",u"B0107无机材料化学",u"B010701无机固体功能材料化学",u"B010702仿生材料化学",u"B0108分离化学",u"B010801萃取化学",u"B010802分离技术与方法",u"B010803无机膜化学与分离",u"B0109核放射化学",u"B010901核化学与核燃料化学",u"B010902放射性药物和标记化合物",u"B010903放射分析化学",u"B010904放射性废物处理和综合利用",u"B0110同位素化学",u"B0111无机纳米化学",u"B0112无机药物化学",u"B0113无机超分子化学",u"B0114有机金属化学",u"B0115原子簇化学",u"B0116应用无机化学",u"B02有机化学",u"B0201有机合成",u"B020101有机合成反应与试剂",u"B020102复杂化合物的设计与合成",u"B020103选择性有机反应",u"B020104催化与不对称反应",u"B020105组合合成",u"B0202金属有机化学",u"B020201金属络合物的合成与反应",u"B020202生物金属有机化学",u"B020203金属有机材料化学",u"B0203元素有机化学",u"B020301有机磷化学",u"B020302有机硅化学",u"B020303有机硼化学",u"B020304有机氟化学",u"B0204天然有机化学",u"B020401甾体及萜类化学",u"B020402中草药与植物化学",u"B020403海洋天然产物化学",u"B020404天然产物合成化学",u"B020405微生物与真菌化学",u"B0205物理有机化学",u"B020501活泼中间体化学",u"B020502有机光化学",u"B020503立体化学基础",u"B020504有机分子结构与反应活性",u"B020505理论与计算有机化学",u"B020506有机超分子与聚集体化学",u"B020507生物物理有机化学",u"B0206药物化学",u"B020601药物分子设计与合成",u"B020602药物构效关系",u"B0207化学生物学与生物有机化学",u"B020701多肽化学",u"B020702核酸化学",u"B020703蛋白质化学",u"B020704糖化学",u"B020705仿生模拟酶与酶化学",u"B020706生物催化与生物合成",u"B0208有机分析",u"B020801有机分析方法",u"B020802手性分离化学",u"B020803生物有机分析",u"B0209应用有机化学",u"B020901农用化学品化学",u"B020902食品化学",u"B020903香料与染料化学",u"B0210绿色有机化学",u"B0211有机分子功能材料化学",u"B021101功能有机分子的设计与合成",u"B021102功能有机分子的组装与性质",u"B021103生物有机功能材料",u"B03物理化学",u"B0301结构化学",u"B030101体相结构",u"B030102表面结构",u"B030103溶液结构",u"B030104动态结构",u"B030105光谱与波谱学",u"B030106纳米及介观结构",u"B030107方法与理论",u"B0302理论和计算化学",u"B030201量子化学",u"B030202化学统计力学",u"B030203化学动力学理论",u"B030204计算模拟方法与应用",u"B0303催化化学",u"B030301多相催化",u"B030302均相催化",u"B030303仿生催化",u"B030304光催化",u"B030305催化表征方法与技术",u"B0304化学动力学",u"B030401宏观动力学",u"B030402分子动态学",u"B030403超快动力学",u"B030404激发态化学",u"B0305胶体与界面化学",u"B030501表面活性剂",u"B030502分散体系与流变性能",u"B030503表面/界面吸附现象",u"B030504超细粉和颗粒",u"B030505分子组装与聚集体",u"B030506表面/界面表征技术",u"B0306电化学",u"B030601电极过程动力学",u"B030602腐蚀电化学",u"B030603材料电化学",u"B030604光电化学",u"B030605界面电化学",u"B030606电催化",u"B030607纳米电化学",u"B030608化学电源",u"B0307光化学和辐射化学",u"B030701超快光谱学",u"B030702材料光化学",u"B030703等离子体化学与应用",u"B030704辐射化学",u"B030705感光化学",u"B030706光化学与光物理过程",u"B0308热力学",u"B030801化学平衡与热力学参数",u"B030802溶液化学",u"B030803量热学",u"B030804复杂流体",u"B030805非平衡态热力学与耗散结构",u"B030806统计热力学",u"B0309生物物理化学",u"B030901结构生物物理化学",u"B030902生物光电化学与热力学",u"B030903生命过程动力学",u"B030904生物物理化学方法与技术",u"B0310化学信息学",u"B031001分子信息学",u"B031002化学反应和化学过程的信息学",u"B031003化学数据库",u"B031004分子信息处理中的算法",u"B04高分子科学",u"B0401高分子合成化学",u"B040101高分子设计与合成",u"B040102配位聚合与离子型聚合",u"B040103高分子光化学与辐射化学",u"B040104生物参与的聚合与降解反应",u"B040105缩聚反应",u"B040106自由基聚合",u"B0402高分子化学反应",u"B040201高分子降解与交联",u"B040202高分子接枝与嵌段",u"B040203高分子改性反应与方法",u"B0403功能与智能高分子",u"B040301吸附与分离功能高分子",u"B040302高分子催化剂和高分子试剂",u"B040303医用与药用高分子",u"B040304生物活性高分子",u"B040305液晶态高分子",u"B040306光电磁功能高分子",u"B040307储能与换能高分子",u"B040308高分子功能膜",u"B040309仿生高分子",u"B0404天然高分子与生物高分子",u"B040401基于可再生资源高分子",u"B0405高分子组装与超分子结构",u"B040501超分子聚合物",u"B040502超支化与树形高分子",u"B0406高分子物理与高分子物理化学",u"B040601高分子溶液",u"B040602高分子聚集态结构",u"B040603高分子转变与相变",u"B040604高分子形变与取向",u"B040605高分子纳米微结构及尺寸效应",u"B040606高分子表面与界面",u"B040607高分子结构与性能关系",u"B040608高分子测试及表征方法",u"B040609高分子流变学",u"B040610聚电解质与高分子凝胶",u"B040611高分子塑性与黏弹性",u"B040612高分子统计理论",u"B040613高分子理论计算与模拟",u"B0407应用高分子化学与物理",u"B040701高分子加工原理与新方法",u"B040702高性能聚合物",u"B040703高分子多相与多组分复合体系",u"B040704聚合反应动力学及聚合反应过程控制",u"B040705杂化高分子",u"B040706高分子循环利用",u"B05分析化学",u"B0501色谱分析",u"B050101气相色谱",u"B050102液相色谱",u"B050103离子色谱与薄层色谱",u"B050104毛细管电泳及电色谱",u"B050105微流控系统与芯片分析",u"B050106色谱柱固定相与填料",u"B0502电化学分析",u"B050201伏安法",u"B050202生物电分析化学",u"B050203化学修饰电极",u"B050204微电极与超微电极",u"B050205光谱电化学分析",u"B050206电化学传感器",u"B050207电致化学发光",u"B0503光谱分析",u"B050301原子发射与吸收光谱",u"B050302原子荧光与X-射线荧光光谱",u"B050303分子荧光与磷光光谱",u"B050304化学发光与生物发光",u"B050305紫外与可见光谱",u"B050306红外与拉曼光谱",u"B050307光声光谱",u"B050308共振光谱",u"B0504波谱分析与成像分析",u"B0505质谱分析",u"B0506分析仪器与试剂",u"B050601联用技术",u"B050602分析仪器关键部件、配件研制",u"B050603分析仪器微型化",u"B050604极端条件下分析技术",u"B0507热分析与能谱分析",u"B0508放射分析",u"B0509生化分析及生物传感",u"B050901单分子、单细胞分析",u"B050902纳米生物化学分析方法",u"B050903药物与临床分析",u"B050904细胞与病毒分析",u"B050905免疫分析化学",u"B050906生物分析芯片",u"B0510活体与复杂样品分析",u"B0511样品前处理方法与技术",u"B0512化学计量学与化学信息学",u"B0513表面、形态与形貌分析",u"B051301表面、界面分析",u"B051302微区分析",u"B051303形态分析",u"B051304扫描探针形貌分析",u"B06化学工程及工业化学",u"B0601化工热力学和基础数据",u"B060101状态方程与溶液理论",u"B060102相平衡",u"B060103化学平衡",u"B060104热力学理论及计算机模拟",u"B060105化工基础数据",u"B0602传递过程",u"B060201化工流体力学和传递性质",u"B060202传热过程及设备",u"B060203传质过程",u"B060204颗粒学",u"B060205非常规条件下的传递过程",u"B0603分离过程",u"B060301蒸馏蒸发与结晶",u"B060302干燥与吸收",u"B060303萃取",u"B060304吸附与离子交换",u"B060305机械分离过程",u"B060306膜分离",u"B060307非常规分离技术",u"B0604化学反应工程",u"B060401化学反应动力学",u"B060402反应器原理及传递特性",u"B060403反应器的模型化和优化",u"B060404流态化技术和多相流反应工程",u"B060405固定床反应工程",u"B060406聚合反应工程",u"B060407电化学反应工程",u"B060408生化反应工程",u"B060409催化剂工程",u"B0605化工系统工程",u"B060501化学过程的控制与模拟",u"B060502化工系统的优化",u"B0606无机化工",u"B060601基础无机化工",u"B060602工业电化学",u"B060603精细无机化工",u"B060604核化工与放射化工",u"B0607有机化工",u"B060701基础有机化工",u"B060702精细有机化工",u"B0608生物化工与食品化工",u"B060801生化反应动力学及反应器",u"B060802生化分离工程",u"B060803生化过程的优化与控制",u"B060804生物催化过程",u"B060805天然产物及农产品的化学改性",u"B060806生物医药工程",u"B060807绿色食品工程与技术",u"B0609能源化工",u"B060901煤化工",u"B060902石油化工",u"B060903燃料电池",u"B060904天然气及碳--化工",u"B060905生物质能源化工",u"B0610化工冶金",u"B0611环境化工",u"B061101环境治理中的物理化学原理",u"B061102三废治理技术中的化工过程",u"B061103环境友好的化工过程",u"B061104可持续发展环境化工的新概念",u"B0612资源化工",u"B061201资源有效利用与循环利用",u"B061202材料制备的化工基础",u"B07环境化学",u"B0701环境分析化学",u"B070101无机污染物分离分析",u"B070102有机污染物分离分析",u"B070103污染物代谢产物分析",u"B070104污染物形态分离分析",u"B0702环境污染化学",u"B070201大气污染化学",u"B070202水污染化学",u"B070203土壤污染化学",u"B070204固体废弃物污染化学",u"B070205放射污染化学",u"B070206纳米材料污染化学",u"B070207复合污染化学",u"B0703污染控制化学",u"B070301大气污染控制化学",u"B070302水污染控制化学",u"B070303土壤污染控制化学",u"B070304固体废弃物污染控制化学",u"B0704污染生态化学",u"B070401污染物赋存形态和生物有效性",u"B070402污染物与生物大分子的相互作用",u"B070403污染物的生态毒性和毒理",u"B0705理论环境化学",u"B070501污染化学动力学",u"B070502污染物构效关系",u"B070503化学计量学在环境化学中的应用",u"B070504环境污染模式与预测",u"B0706区域环境化学",u"B070601化学污染物的源汇识别",u"B070602污染物的区域环境化学过程",u"B070603污染物输送中的化学机制",u"B0707化学环境污染与健康",u"B070701环境污染的生物标志物",u"B070702环境污染与食品安全",u"B070703人居环境与健康",u"B070704环境暴露与毒理学",u"C生命科学部",u"C01微生物学",u"C0101微生物资源与分类学",u"C010101细菌资源、分类与系统发育",u"C010102放线菌资源、分类与系统发育",u"C010103真菌资源、分类与系统发育",u"C010104病毒资源与分类",u"C0102微生物生理与生物化学",u"C010201微生物生理与代谢",u"C010202微生物生物化学",u"C0103微生物遗传育种学",u"C010301微生物功能基因",u"C010302微生物遗传育种",u"C0104微生物学研究的新技术与新方法",u"C0105环境微生物学",u"C010501陆生环境微生物学",u"C010502水生环境微生物学",u"C010503其他环境微生物学",u"C0106病原细菌与放线菌生物学",u"C010601植物病原细菌与放线菌生物学",u"C010602动物病原细菌与放线菌生物学",u"C010603人类病原细菌与放线菌生物学",u"C0107病原真菌学",u"C010701植物病原真菌学",u"C010702动物病原真菌学",u"C010703人类病原真菌学",u"C0108病毒学",u"C010801植物病毒学",u"C010802动物病毒学",u"C010803人类病毒学",u"C010804噬菌体",u"C0109支原体、立克次体与衣原体",u"C010901支原体",u"C010902立克次体、衣原体等",u"C02植物学",u"C0201植物结构学",u"C020101植物形态结构与功能",u"C020102植物形态与发生",u"C0202植物分类学",u"C020201种子植物分类",u"C020202孢子植物分类",u"C020203植物地理学",u"C0203植物进化生物学",u"C020301植物系统发育",u"C020302古植物学与孢粉学",u"C020303植物进化与发育",u"C0204植物生理与生化",u"C020401光合作用",u"C020402生物固氮",u"C020403呼吸作用",u"C020404矿质元素与代谢",u"C020405有机物质合成与运输",u"C020406水分生理",u"C020407抗性生理",u"C020408植物激素与生长发育",u"C020409植物次生代谢与调控",u"C020410种子生理",u"C0205植物生殖生物学",u"C020501植物配子体发生与受精",u"C020502植物胚胎发生",u"C0206植物资源学",u"C020601植物资源评价",u"C020602植物引种驯化",u"C020603植物种质",u"C020604植物化学",u"C020605水生植物与资源",u"C0207植物学研究的新技术、新方法",u"C03生态学",u"C0301分子与进化生态学",u"C030101分子生态学",u"C030102进化生态学",u"C0302行为生态学",u"C030201昆虫行为生态学",u"C030202其他动物行为生态学",u"C0303生理生态学",u"C030301植物生理生态学",u"C030302动物生理生态学",u"C0304种群生态学",u"C030401植物种群生态学",u"C030402昆虫种群生态学",u"C030403其他动物种群生态学",u"C0305群落生态学",u"C030501群落结构与动态",u"C030502物种间相互作用",u"C0306生态系统生态学",u"C030601农田生态学",u"C030602森林生态学",u"C030603草地与荒漠生态",u"C030604水域生态学",u"C0307景观与区域生态学",u"C030701景观生态学",u"C030702区域生态学",u"C0308全球变化生态学",u"C030801陆地生态系统与全球变化",u"C030802海洋生态系统与全球变化",u"C0309微生物生态学",u"C0310污染生态学",u"C031001污染生态学",u"C031002毒理生态学",u"C0311土壤生态学",u"C031101土壤生态系统水分、养分循环",u"C031102土壤生物与土壤生态系统",u"C0312保护生物学与恢复生态学",u"C031201生物多样性",u"C031202保护生物学",u"C031203受损生态系统恢复",u"C0313生态安全评价",u"C031301转基因生物的生态安全性评价",u"C031302外来物种的入侵与生态安全性评价",u"C031303生态工程评价",u"C04林学",u"C0401森林资源学",u"C0402森林资源信息学",u"C040201森林资源管理与信息技术",u"C040202森林灾害监测的理论与方法",u"C0403木材物理学",u"C040301材性及其改良",u"C040302木材加工学",u"C040303人工复合木材",u"C0404林产化学",u"C040401树木化学成分分析",u"C040402造纸与制浆",u"C0405森林生物学",u"C040501树木生长发育",u"C040502树木抗逆生理学",u"C040503树木繁殖生物学",u"C0406森林土壤学",u"C0407森林培育学",u"C040701森林植被恢复与保持",u"C040702人工林培育",u"C040703种苗学",u"C040704复合农林业",u"C0408森林经理学",u"C040801森林可持续发展",u"C040802森林分类经营",u"C0409森林健康",u"C040901森林病理",u"C040902森林害虫",u"C040903森林防火",u"C0410林木遗传育种学",u"C041001林木种质资源",u"C041002林木遗传改良",u"C041003林木育种理论与方法",u"C0411经济林学",u"C041101经济林重要形状形成及调控",u"C041102经济林栽培生理",u"C041103林木果实采后生物学",u"C041104茶学",u"C0412园林学",u"C041201园林植物种质资源",u"C041202城市园林与功能",u"C041203园林规划和景观设计",u"C0413荒漠化与水土保持",u"C041301防护林学",u"C041302森林植被与水土保持",u"C041303植被与荒漠化",u"C0414林业研究的新技术与新方法",u"C05生物物理、生物化学与分子生物学",u"C0501生物大分子结构与功能",u"C050101生物大分子结构计算与理论预测",u"C050102生物大分子空间结构测定",u"C050103生物大分子相互作用",u"C0502生物化学",u"C050201蛋白质与多肽生物化学",u"C050202核酸生物化学",u"C050203酶学",u"C050204糖生物学",u"C050205无机生物化学",u"C0503蛋白质组学",u"C0504膜生物化学与膜生物物理学",u"C050401生物膜结构与功能",u"C050402跨膜信号转导",u"C050403物质跨膜转运",u"C050404其他膜生物化学与膜生物物理学",u"C0505系统生物学",u"C0506环境生物物理",u"C050601电磁辐射生物物理",u"C050602声生物物理",u"C050603光生物物理",u"C050604电离辐射生物物理与放射生物学",u"C050605自由基生物学",u"C0507空间生物学",u"C0508生物物理、生物化学与分子生物学研究的新方法与新技术",u"C06遗传学与发育生物学",u"C0601植物遗传学",u"C060101植物分子遗传",u"C060102植物细胞遗传",u"C060103植物数量遗传",u"C0602动物遗传学",u"C060201动物分子遗传",u"C060202动物细胞遗传",u"C060203动物数量遗传",u"C0603微生物遗传学",u"C060301原核微生物遗传",u"C060302真核微生物遗传",u"C0604人类遗传学",u"C060401人类遗传的多样性",u"C060402人类起源与进化",u"C060403人类行为的遗传基础",u"C060404人类表型性状与遗传",u"C0605医学遗传学",u"C060501单基因遗传病的遗传基础",u"C060502多基因遗传病的遗传基础",u"C060503线粒体与疾病",u"C060504染色体异常与疾病",u"C060505肿瘤遗传",u"C060506遗传病模型",u"C0606基因组学",u"C060601基因组结构与分析",u"C060602比较基因组与进化",u"C060603基因组信息学",u"C0607基因表达调控与表观遗传学",u"C060701组蛋白修饰及意义",u"C060702DNA修饰及意义",u"C060703染色体重塑及意义",u"C060704非编码RNA调控与功能",u"C060705转录与调控",u"C0608生物信息学",u"C060801生物数据分析",u"C060802生物信息算法及工具",u"C060803生物信息挖掘",u"C060804生物系统网络模型",u"C0609遗传学研究新方法",u"C0610发育生物学",u"C061001性器官与性细胞发育",u"C061002精卵识别与受精",u"C061003胚胎早期发育",u"C061004组织、器官的形成与发育",u"C061005组织、器官的维持与再生",u"C061006细胞的分化与发育",u"C061007核质互作与重编程",u"C061008干细胞及定向分化基础",u"C061009模式生物与发育",u"C061010发育研究新方法与体系",u"C07细胞生物学",u"C0701细胞、亚细胞结构与功能",u"C0702细胞生长与分裂",u"C0703细胞周期与调控",u"C0704细胞增殖与分化",u"C0705细胞衰老",u"C0706细胞死亡",u"C0707细胞运动",u"C0708细胞外基质",u"C0709细胞信号转导",u"C0710人体解剖学",u"C0711人体组织与胚胎学",u"C071101人体组织学",u"C071102人体胚胎学",u"C08免疫学",u"C0801免疫生物学",u"C080101分子免疫",u"C080102细胞免疫",u"C080103免疫应答",u"C080104免疫耐受",u"C080105免疫调节",u"C0802免疫遗传学",u"C0803免疫病理学",u"C0804神经内分泌免疫学",u"C0805生殖免疫学",u"C0806黏膜免疫学",u"C0807临床免疫学",u"C080701自身免疫与自身免疫性疾病",u"C080702超敏反应与超敏反应性疾病",u"C080703免疫缺陷与免疫缺陷性疾病",u"C080704其他免疫性疾病",u"C0808感染免疫学",u"C080801病毒与免疫",u"C080802细菌与免疫",u"C080803真菌与免疫",u"C080804寄生虫与免疫",u"C0809肿瘤免疫学",u"C0810移植免疫学",u"C0811器官移植学",u"C0812免疫预防学",u"C0813免疫诊断学",u"C0814疫苗学",u"C081401疫苗设计",u"C081402疫苗佐剂",u"C081403疫苗递送系统",u"C081404疫苗效应及机制",u"C0815抗体工程学",u"C081501抗体与功能",u"C081502重组与改型",u"C081503抗体的高效表达系统",u"C0816免疫学新技术新方法",u"C09神经科学与心理学",u"C0901心理学",u"C090101认知心理学",u"C090102生理心理学",u"C090103医学心理学",u"C090104精神卫生学",u"C090105工程心理学",u"C090106发展心理学",u"C090107教育心理学",u"C090108社会心理学",u"C090109应用心理学",u"C0902神经生物学",u"C090201分子神经生物学",u"C090202细胞神经生物学",u"C090203发育神经生物学",u"C090204系统神经生物学",u"C090205认知神经生物学",u"C090206计算神经生物学",u"C090207感觉系统神经生物学",u"C0903神经和精神系统疾病",u"C090301神经病学",u"C090302精神病学",u"C10生物医学工程学",u"C1001生物力学与生物流变学",u"C100101生物力学",u"C100102生物流变学",u"C1002生物材料与组织工程学",u"C100201生物材料",u"C100202组织工程",u"C100203人工器官",u"C1003仿生学",u"C1004生物医学电子学",u"C100401生物医学信号检测与处理",u"C100402生物系统建模及仿真",u"C100403生物医学器件与仪器",u"C100404生物传感",u"C1005生物医学图像与成像",u"C100501生物医学图像",u"C100502医学信息系统",u"C100503生物医学成像",u"C1006纳米生物学与纳米医学",u"C100601纳米生物学",u"C100602纳米医学",u"C1007医学影像学",u"C100701影像诊断学",u"C100702生物医学超声",u"C100703核医学",u"C100704医学影像物理与工程",u"C1008放射医学",u"C100801放射治疗学",u"C100802放射病理学",u"C100803放射生物学",u"C100804放射防护学",u"C1009生物医学工程研究的新技术与新方法",u"C11农学",u"C1101农学基础",u"C110101农业数学与农业物理",u"C110102农业气象学",u"C110103农业水土资源利用学",u"C110104农业信息学",u"C110105农业系统工程",u"C1102作物学",u"C110201作物生理学",u"C110202作物栽培与耕作学",u"C110203稻类作物种质资源与遗传育种",u"C110204麦类作物种质资源与遗传育种",u"C110205玉米作物种质资源与遗传育种",u"C110206油料作物种质资源与遗传育种",u"C110207棉麻类作物种质资源与遗传育种",u"C110208其他作物种质资源与遗传育种",u"C110209作物种子学",u"C110210作物遗传育种的理论与方法",u"C1103植物营养学",u"C110301植物营养遗传",u"C110302植物营养生理",u"C110303肥料与施肥科学",u"C110304养分资源与养分循环",u"C110305作物－土壤互作过程与调控",u"C1104植物保护学",u"C110401植物病虫害测报学",u"C110402植物病理学的理论与方法",u"C110403植物真菌病害与防治",u"C110404植物细菌病害与防治",u"C110405植物病毒病害与防治",u"C110406植物其他病害与防治",u"C110407农业昆虫与害虫防治",u"C110408杂草防治",u"C110409鼠害防治",u"C110410农业有害生物检疫学",u"C110411化学保护",u"C110412植物病害生物防治",u"C110413植物害虫生物防治",u"C1105园艺学",u"C110501果树学",u"C110502蔬菜学",u"C110503瓜果学",u"C110504观赏园艺学",u"C110505设施园艺学",u"C1106农作物产品贮藏、保鲜与安全",u"C110601农作物产品贮藏保鲜的理论与方法",u"C110602农作物产品的品质与营养",u"C110603农作物产品安全",u"C110604果蔬贮藏与保鲜",u"C110605食用真菌",u"C12畜牧兽医与水产学",u"C1201畜牧学",u"C120101畜禽资源",u"C120102畜禽遗传育种学",u"C120103畜禽繁殖学",u"C120104动物营养学",u"C120105饲料学",u"C120106畜禽行为学",u"C120107畜禽环境学",u"C120108畜产品加工学",u"C120109草原学",u"C120110养蚕学",u"C120111养蜂学",u"C1202兽医学",u"C120201畜禽组织与解剖学",u"C120202畜禽生理生化",u"C120203动物病理学",u"C120204兽医免疫学",u"C120205兽医寄生虫学",u"C120206兽医传染病学",u"C120207中兽医学",u"C120208兽医药理学与毒理学",u"C120209临床兽医学",u"C1203水产学",u"C120301水产生物生理学",u"C120302水产生物遗传育种学",u"C120303水产资源与保护学",u"C120304水产生物营养学",u"C120305水产养殖学",u"C120306水产生物病害与控制",u"C120307水产品加工与保鲜",u"C120308水产品安全与质量控制",u"C1204动物食品科学",u"C120401动物产品的贮藏、保鲜",u"C120402动物产品的品质与营养",u"C120403动物产品的安全",u"C13动物学",u"C1301动物形态学及胚胎学",u"C1302动物系统及分类学",u"C130201动物分类学",u"C130202动物系统学",u"C130203动物地理学",u"C130204动物进化",u"C1303动物生理及行为学",u"C130301动物生理生化",u"C130302动物行为学",u"C1304动物资源与保护",u"C1305昆虫学",u"C130501昆虫系统及分类学",u"C130502昆虫形态学",u"C130503昆虫行为学",u"C130504昆虫生理生化",u"C130505昆虫毒理学",u"C130506昆虫资源与保护",u"C1306实验动物学",u"C130601实验动物",u"C130602模式动物",u"C14生理学与病理学",u"C1401人体生理学",u"C140101循环生理学",u"C140102血液及淋巴生理学",u"C140103呼吸生理学",u"C140104消化生理学",u"C140105泌尿生理学",u"C140106内分泌及代谢生理学",u"C140107生殖生理学",u"C1402人体病理学",u"C140201心血管系统病理学",u"C140202血液及淋巴系统病理学",u"C140203呼吸系统病理学",u"C140204消化系统病理学",u"C140205泌尿系统病理学",u"C140206内分泌及代谢系统病理学",u"C140207生殖系统病理学",u"C140208肿瘤病理学",u"C140209实验病理学",u"C1403病理生理学",u"C140301疾病与离子通道",u"C140302疾病与受体",u"C140303炎症",u"C140304组织重构",u"C140305缺血缺氧",u"C140306休克与微循环",u"C140307应激、适应与代偿",u"C140308疾病与血管新生",u"C1404内科学",u"C140401心血管系统疾病",u"C140402血液与淋巴系统疾病",u"C140403呼吸系统疾病",u"C140404消化系统疾病",u"C140405泌尿系统疾病",u"C140406内分泌学与代谢病",u"C1405运动医学",u"C140501运动生理与生化",u"C140502运动损伤与修复",u"C1406特种医学",u"C140601特殊环境生理学",u"C140602特殊环境病理学",u"C140603特种环境相关疾病",u"C15预防医学",u"C1501环境与职业卫生学",u"C150101环境卫生学",u"C150102职业卫生学",u"C1502营养与食品卫生学",u"C150201营养学",u"C150202食品卫生学",u"C1503妇幼与儿童少年卫生学",u"C150301妇幼卫生学",u"C150302儿童少年卫生学",u"C1504卫生毒理学",u"C1505流行病学与卫生统计学",u"C150501传染病流行病学",u"C150502非传染病流行病学",u"C150503流行病学方法学及卫生统计学",u"C1506地方病学",u"C1507传染病学",u"C150701传染病媒介生物",u"C150702寄生虫性传染病",u"C150703病毒性传染病",u"C150704细菌性传染病",u"C150705其他病原体引起的传染病",u"C1508皮肤性病学",u"C150801皮肤病",u"C150802性传播疾病",u"C16临床医学基础Ⅰ",u"C1601诊断学与治疗学基础",u"C160101物理诊断学",u"C160102检验医学",u"C160103物理治疗学基础",u"C1602麻醉学",u"C160201麻醉学基础",u"C160202镇痛",u"C160203脏器保护与复苏",u"C160204体外循环",u"C1603外科学基础",u"C160301外科营养与代谢",u"C160302外科感染",u"C1604普通外科学",u"C160401胃肠、肛管疾病",u"C160402肝、胆、胰疾病",u"C160403乳腺疾病",u"C160404甲状腺疾病",u"C160405血管外科和淋巴管疾病",u"C160406腹部脏器移植",u"C160407腹部其他组织器官疾病",u"C1605心胸外科学",u"C160501胸部外伤",u"C160502成人心脏外科学",u"C160503先天性心脏病学",u"C160504胸部其他组织器官疾病",u"C160505心肺移植和辅助循环学",u"C1606泌尿外科学",u"C160601结石",u"C160602尿动力学",u"C160603男科学",u"C160604泌尿系统脏器移植",u"C160605前列腺疾病",u"C160606泌尿系统畸形、损伤、炎症等",u"C1607骨外科学",u"C160701脊柱外科",u"C160702关节外科",u"C160703手外科与外周神经修复",u"C160704骨质疏松",u"C160705骨创伤",u"C160706骨与关节感染",u"C1608神经外科学",u"C160801功能神经外科",u"C160802损伤、修复、移植",u"C160803脑血管疾病",u"C1609创伤与烧伤外科学",u"C160901创伤学",u"C160902烧伤学",u"C1610整形外科学",u"C161001创面愈合与瘢痕",u"C161002体表组织器官畸形",u"C1611小儿外科学",u"C1612老年医学",u"C161201衰老生理学",u"C161202衰老病理学",u"C1613康复医学",u"C17临床医学基础Ⅱ",u"C1701妇科学",u"C1702生殖医学",u"C1703产科学",u"C1704围生医学",u"C1705儿科学",u"C1706眼科学",u"C170601角膜及眼表疾病",u"C170602眼底疾病",u"C170603视神经及视路相关疾病",u"C170604眼科其他疾病",u"C1707耳鼻喉科学",u"C170701鼻和前颅底疾病",u"C170702咽喉及颈部疾病",u"C170703耳和侧颅底疾病",u"C1708口腔医学",u"C170801口腔内科学",u"C170802口腔颌面外科学",u"C170803口腔修复学",u"C170804口腔正畸学",u"C1709法医学",u"C1710肿瘤学",u"C171001肿瘤研究体系与方法",u"C171002肿瘤病因",u"C171003肿瘤诊断",u"C171004肿瘤预防",u"C171005肿瘤化学药物治疗",u"C171006肿瘤物理治疗",u"C171007肿瘤生物治疗",u"C171008肿瘤综合治疗",u"C171009肿瘤分子靶向治疗",u"C171010抗肿瘤转移与复发",u"C18药物学与药理学",u"C1801药理学",u"C180101神经精神药物药理学",u"C180102心脑血管药物药理学",u"C180103老年病药物药理学",u"C180104抗炎与免疫药物药理学",u"C180105抗肿瘤药物药理学",u"C180106抗病毒药物药理学",u"C180107代谢性疾病药物药理学",u"C180108消化与呼吸系统药物药理学",u"C180109血液、泌尿与生殖系统药物药理学",u"C180110药物代谢与药物动力学",u"C180111临床药理学",u"C180112药物毒理学",u"C1802药物学",u"C180201合成药物化学",u"C180202天然药物化学",u"C180203药物设计与药物信息学",u"C180204药剂学",u"C180205生物药物",u"C180206药物分析学",u"C180207海洋药物学",u"C180208药物材料学",u"C180209特种药物学",u"C19中医学与中药学",u"C1901中医基础理论",u"C190101脏腑气血津液体质",u"C190102病因病机",u"C190103证候基础研究",u"C190104治则与治法",u"C190105中医方剂学",u"C190106中医诊断学",u"C190107经络学与腧穴学",u"C1902中医临床基础",u"C190201中医内科学",u"C190202中医外科学",u"C190203中医骨伤科学",u"C190204中医妇科学",u"C190205中医儿科学",u"C190206中医眼科学",u"C190207中医耳鼻喉科学",u"C190208中医口腔科学",u"C190209中医老年病学",u"C190210中医养生与康复",u"C1903针灸学",u"C190301中医针灸学",u"C190302按摩推拿学",u"C1904中西医结合",u"C190401中西医结合基础理论",u"C190402中西医结合临床基础",u"C1905中药化学",u"C1906中药资源与鉴定学",u"C190601道地药材",u"C190602种质资源评价",u"C190603药材质量评价",u"C190604中药鉴定学",u"C1907中药药理学",u"C190701神经精神药理",u"C190702心脑血管药理",u"C190703抗肿瘤药理",u"C190704内分泌及代谢药理",u"C190705抗炎与免疫药理",u"C190706抗病毒药理",u"C190707消化与呼吸药理",u"C190708泌尿与生殖药理",u"C190709中药药代动力学",u"C190710中药毒理学",u"C1908中药药性与炮制学",u"C190801中药炮制学",u"C190802中药药性理论研究",u"C1909中药制剂学",u"C1910民族医药学",u"C191001民族医学",u"C191002民族药学",u"C1911中医药学研究的新方法、新技术",u"D地球科学部",u"D01地理学",u"D0101自然地理学",u"D010101地貌学",u"D010102水文学",u"D010103应用气候学",u"D010104生物地理学",u"D010105冰冻圈地理学",u"D010106综合自然地理学",u"D0102人文地理学",u"D010201经济地理学",u"D010202社会、文化地理学",u"D010203城市地理学",u"D010204乡村地理学",u"D0103景观地理学",u"D0104环境变化与预测",u"D0105土壤学",u"D010501土壤地理学",u"D010502土壤物理学",u"D010503土壤化学",u"D010504土壤生物学",u"D010505土壤侵蚀与水土保持",u"D010506土壤肥力与土壤养分循环",u"D010507土壤污染与修复",u"D010508土壤质量与食物安全",u"D0106遥感机理与方法",u"D0107地理信息系统",u"D010701空间数据组织与管理",u"D010702遥感信息分析与应用",u"D010703空间定位数据分析与应用",u"D0108测量与地图学",u"D0109污染物行为过程及其环境效应",u"D010901污染物迁移、转化、归趋动力学",u"D010902污染物生物有效性与生态毒理",u"D010903污染物区域空间过程与生态风险",u"D0110区域环境质量与安全",u"D011001区域环境质量综合评估",u"D011002自然灾害风险评估与公共安全",u"D011003重大工程活动的影响",u"D011004生态恢复及其环境效应",u"D0111自然资源管理",u"D011101可再生资源演化",u"D011102自然资源评价",u"D011103自然资源利用与规划",u"D0112区域可持续发展",u"D011201资源与可持续发展",u"D011202经济发展与环境质量",u"D011203可持续性评估",u"D02地质学",u"D0201古生物学和古生态学",u"D020101古生物学",u"D020102古人类学",u"D020103古生态学",u"D020104地球环境与生命演化",u"D0202地层学",u"D0203矿物学(含矿物物理学）",u"D0204岩石学",u"D0205矿床学",u"D0206沉积学和盆地动力学",u"D0207石油、天然气地质学",u"D0208煤地质学",u"D0209第四纪地质学",u"D0210前寒武纪地质学",u"D0211构造地质学与活动构造",u"D021101构造地质学",u"D021102活动构造",u"D021103构造物理与流变学",u"D0212大地构造学",u"D0213水文地质学(含地热地质学)",u"D0214工程地质学",u"D0215数学地质学与遥感地质学",u"D0216火山学",u"D0217生物地质学",u"D0218环境地质学和灾害地质学",u"D03地球化学",u"D0301同位素地球化学",u"D0302微量元素地球化学",u"D0303岩石地球化学",u"D0304矿床地球化学和有机地球化学",u"D0305同位素和化学年代学",u"D0306实验地球化学和计算地球化学",u"D0307宇宙化学与比较行星学",u"D0308生物地球化学",u"D0309环境地球化学",u"D04地球物理学和空间物理学",u"D0401大地测量学",u"D040101物理大地测量学",u"D040102动力大地测量学",u"D040103卫星大地测量学（含导航学）",u"D0402地震学",u"D0403地磁学",u"D0404地球电磁学",u"D0405重力学",u"D0406地热学",u"D0407地球内部物理学",u"D0408地球动力学",u"D0409应用地球物理学",u"D040901勘探地球物理学",u"D040902城市地球物理",u"D0410空间物理",u"D041001高层大气物理学",u"D041002电离层物理学",u"D041003磁层物理学",u"D041004太阳大气和行星际物理学",u"D041005宇宙线物理学",u"D041006行星物理学",u"D0411地球物理实验与仪器",u"D0412空间环境和空间天气",u"D05大气科学",u"D0501对流层大气物理学",u"D0502边界层大气物理学和大气湍流",u"D0503大气遥感和大气探测",u"D0504中层与行星大气物理学",u"D0505天气学",u"D0506大气动力学",u"D0507气候学与气候系统",u"D0508数值预报与数值模拟",u"D0509应用气象学",u"D0510大气化学",u"D0511云雾物理化学与人工影响天气",u"D0512大气环境与全球气候变化",u"D0513气象观测原理、方法及数据分析",u"D06海洋科学",u"D0601物理海洋学",u"D0602海洋物理学",u"D0603海洋地质学",u"D0604海洋化学",u"D0605河口海岸学",u"D0606工程海洋学",u"D0607海洋监测、调查技术",u"D0608海洋环境科学",u"D0609生物海洋学与海洋生物资源",u"D0610海洋遥感",u"D0611极地科学",u"E工程与材料科学部",u"E01金属材料",u"E0101金属结构材料",u"E010101新型金属结构材料",u"E010102钢铁和有色合金结构材料",u"E0102金属基复合材料",u"E010201纤维、颗粒增强金属基复合材料",u"E010202新型金属基复合材料",u"E0103金属非晶态、准晶和纳米晶材料",u"E010301非晶态金属材料",u"E010302纳米晶金属材料",u"E010303新型亚稳金属材料",u"E0104极端条件下使用的金属材料",u"E0105金属功能材料",u"E010501金属磁性材料",u"E010502金属智能材料",u"E010503新型金属功能材料",u"E0106金属材料的合金相、相变及合金设计",u"E010601金属材料的合金相图",u"E010602金属材料的合金相变",u"E010603金属材料的合金设计",u"E0107金属材料的微观结构",u"E010701金属的晶体结构与缺陷及其表征方法",u"E010702金属材料的界面问题",u"E0108金属材料的力学行为",u"E010801金属材料的形变与损伤",u"E010802金属材料的疲劳与断裂",u"E010803金属材料的强化与韧化",u"E0109金属材料的凝固与结晶学",u"E010901金属的非平衡凝固与结晶",u"E010902金属的凝固行为与结晶理论",u"E0110金属材料表面科学与工程",u"E011001金属材料表面的组织、结构与性能",u"E011002金属材料表面改性及涂层",u"E0111金属材料的腐蚀与防护",u"E011101金属常温腐蚀与防护",u"E011102金属高温腐蚀与防护",u"E0112金属材料的磨损与磨蚀",u"E011201金属材料的摩擦磨损",u"E011202金属材料的磨蚀",u"E0113金属材料的制备科学与跨学科应用基础",u"E02无机非金属材料",u"E0201人工晶体",u"E0202玻璃材料",u"E020201特种玻璃材料",u"E020202传统玻璃材料",u"E0203结构陶瓷",u"E020301先进结构陶瓷",u"E020302陶瓷基复合材料",u"E0204功能陶瓷",u"E020401精细功能陶瓷",u"E020402压电与铁电陶瓷材料",u"E020403生物陶瓷与生物材料",u"E020404功能类陶瓷复合材料",u"E0205水泥与耐火材料",u"E020501新型水泥材料",u"E020502新型耐火材料",u"E0206碳素材料与超硬材料",u"E020601高性能碳素材料",u"E020602金刚石及其他超硬材料",u"E020603新型碳功能材料",u"E0207无机非金属类光电信息与功能材料",u"E020701微电子与光电子材料",u"E020702发光及显示材料",u"E020703特种无机涂层与薄膜",u"E0208无机非金属基复合材料",u"E020801复合材料的制备",u"E020802强化与增韧理论",u"E020803界面物理与界面化学",u"E0209半导体材料",u"E0210无机非金属类电介质与电解质材料",u"E0211无机非金属类高温超导与磁性材料",u"E021101高温超导材料",u"E021102磁性材料及巨磁阻材料",u"E0212古陶瓷与传统陶瓷",u"E0213其他无机非金属材料",u"E021301生态环境材料",u"E021302无机非金属材料设计及相图",u"E021303无机非金属智能材料",u"E03有机高分子材料",u"E0301塑料",u"E030101设计与制备",u"E030102高性能塑料与工程塑料",u"E0302橡胶及弹性体",u"E030201设计与制备",u"E030202高性能橡胶",u"E030203热塑弹性体",u"E0303纤维",u"E030301设计与制备",u"E030302高性能纤维与特种合成纤维",u"E030303仿生与差别化纤维",u"E0304涂料",u"E0305黏合剂",u"E0306高分子助剂",u"E0307聚合物共混与复合材料",u"E030701材料的设计与制备",u"E030702高性能基体树脂",u"E030703纳米复合",u"E030704增强与增韧",u"E0308特殊与极端环境下的高分子材料",u"E0309有机高分子功能材料",u"E030901光电磁信息功能材料",u"E030902分离与吸附材料",u"E030903感光材料",u"E030904自组装有机材料与图形化",u"E030905有机无机复合功能材料",u"E030906纳米效应与纳米技术",u"E0310生物医用高分子材料",u"E031001组织工程材料",u"E031002载体与缓释材料",u"E031003植入材料",u"E0311智能材料",u"E0312仿生材料",u"E0313高分子材料与环境",u"E031301天然高分子材料",u"E031302环境友好高分子材料",u"E031303高分子材料的循环利用与资源化",u"E031304高分子材料的稳定与老化",u"E0314高分子材料结构与性能",u"E031401结构与性能关系",u"E031402高分子材料的表征与评价",u"E031403高分子材料的表面与界面",u"E0315高分子材料的加工与成型",u"E031501加工与成型中的化学与物理问题",u"E031502加工与成型新原理、新方法",u"E04冶金与矿业",u"E0401金属与非金属地下开采",u"E0402煤炭地下开采",u"E0403石油天然气开采",u"E0404化石能源储存与输送",u"E0405露天开采与边坡工程",u"E0406海洋、空间及其他矿物资源开采与利用",u"E0407钻井工程与地热开采",u"E0408地下空间工程",u"E0409矿山岩体力学与岩层控制",u"E0410安全科学与工程",u"E041001通风与防尘",u"E041002突水与防灭火",u"E041003岩爆与瓦斯灾害",u"E041004安全检测与监控",u"E0411矿物工程与物质分离科学",u"E041101工艺矿物学与粉碎工程学",u"E041102矿物加工工程",u"E041103物理方法分离",u"E041104化学方法分离",u"E041105矿物材料与应用",u"E0412冶金物理化学与冶金原理",u"E041201火法冶金",u"E041202湿法冶金",u"E041203电（化学）冶金与电池电化学",u"E041204冶金熔体(溶液)",u"E041205冶金物理化学研究方法与测试技术",u"E0413冶金化工与冶金反应工程学",u"E0414钢铁冶金",u"E0415有色金属冶金",u"E041501轻金属",u"E041502重金属",u"E041503稀有金属",u"E041504贵金属等分离提取",u"E0416材料冶金过程工程",u"E041601材料冶金物理化学",u"E041602金属净化与提纯",u"E041603熔化、凝固过程与控制",u"E041604金属成形与加工",u"E041605应变冶金",u"E041606喷射与喷涂冶金",u"E041607焊接冶金",u"E041608电磁冶金",u"E0417粉末冶金与粉体工程",u"E0418特殊冶金、外场冶金与冶金新理论、新方法",u"E0419资源循环科学",u"E0420矿冶生态与环境工程",u"E042001矿山复垦与生态恢复",u"E042002矿冶环境污染评测与控制",u"E042003有害辐射等污染的防治",u"E042004绿色冶金与增值冶金",u"E0421矿冶装备工艺原理",u"E0422资源利用科学及其他",u"E042201短流程新技术",u"E042202冶金耐火与保温材料",u"E042203交叉学科与新技术",u"E042204冶金计量、测试与标准",u"E042205矿冶系统工程与信息工程",u"E042206冶金燃烧与节能工程",u"E042207冶金史及古代矿物科学",u"E05机械工程",u"E0501机构学与机器人",u"E050101机构学与机器组成原理",u"E050102机构运动学与动力学",u"E050103机器人机械学",u"E0502传动机械学",u"E050201机械传动",u"E050202流体传动",u"E050203复合传动",u"E0503机械动力学",u"E050301振动/噪声测试、分析与控制",u"E050302机械系统动态监测、诊断与维护",u"E050303机械结构与系统动力学",u"E0504机械结构强度学",u"E050401机械结构损伤、疲劳与断裂",u"E050402机械结构强度理论与可靠性设计",u"E050403机械结构安全评定",u"E0505机械摩擦学与表面技术",u"E050501机械摩擦、磨损与控制",u"E050502机械润滑、密封与控制",u"E050503机械表面效应与表面技术",u"E050504工程摩擦学与摩擦学设计",u"E0506机械设计学",u"E050601设计理论与方法",u"E050602概念设计与优化设计",u"E050603智能设计与数字化设计",u"E050604机械系统集成设计",u"E0507机械仿生学",u"E050701机械仿生原理",u"E050702仿生机械设计与制造",u"E050703人－机－环境工程学",u"E0508零件成形制造",u"E050801铸造工艺与装备",u"E050802塑性加工工艺、模具与装备",u"E050803焊接结构、工艺与装备",u"E050804近净成形与快速制造",u"E0509零件加工制造",u"E050901切削、磨削加工工艺与装备",u"E050902非传统加工工艺与装备",u"E050903超精密加工工艺与装备",u"E050904高能束加工工艺与装备",u"E0510制造系统与自动化",u"E051001数控技术与装备",u"E051002数字化制造与智能制造",u"E051003可重构制造系统",u"E051004可持续设计与制造",u"E051005制造系统调度、规划与管理",u"E0511机械测试理论与技术",u"E051101机械计量标准、理论与方法",u"E051102机械测试理论、方法与技术",u"E051103机械传感器技术与测试仪器",u"E051104机械制造过程监测与控制",u"E0512微/纳机械系统",u"E051201微/纳机械驱动器与执行器件",u"E051202微/纳机械传感与控制",u"E051203微/纳制造过程检测与控制",u"E051204微/纳机械系统组成原理与集成",u"E06工程热物理与能源利用",u"E0601工程热力学",u"E060101热力学基础",u"E060102热力过程与热力循环",u"E060103能源利用系统与评价",u"E060104节能与储能中的工程热物理问题",u"E060105制冷",u"E060106热力系统动态特性、诊断与控制",u"E0602内流流体力学",u"E060201黏性流动与湍流",u"E060202动力装置内部流动",u"E060203流体机械内部流动",u"E060204流体噪声与流固耦合",u"E0603传热传质学",u"E060301热传导",u"E060302辐射换热",u"E060303对流传热传质",u"E060304相变传递过程",u"E060305微观传递过程",u"E0604燃烧学",u"E060401层流火焰和燃烧反应动力学",u"E060402湍流火焰",u"E060403煤与其他固体燃料的燃烧",u"E060404气体、液体燃料燃烧",u"E060405动力装置中的燃烧",u"E060406特殊环境与条件下燃烧",u"E060407燃烧污染物生成和防治",u"E060408火灾",u"E0605多相流热物理学",u"E060501离散相动力学",u"E060502多相流流动",u"E060503多相流传热传质",u"E060504气固两相流",u"E0606热物性与热物理测试技术",u"E060601流体热物性",u"E060602固体材料热物性",u"E060603单相与多相流动测试技术",u"E060604传热传质测试技术",u"E060605燃烧测试技术",u"E0607可再生与替代能源利用中的工程热物理问题",u"E060701太阳能利用中的工程热物理问题",u"E060702生物质能利用中的工程热物理问题",u"E060703风能利用中的工程热物理问题",u"E060704水能、海洋能、潮汐能利用中的工程热物理问题",u"E060705地热能利用中的工程热物理问题",u"E060706氢能利用中的工程热物理问题",u"E0608工程热物理相关交叉领域",u"E07电气科学与工程",u"E0701电磁场与电路",u"E070101电磁场分析与综合",u"E070102电网络理论",u"E070103静电理论与技术",u"E070104电磁测量与传感",u"E0702电工材料特性及其应用",u"E070201工程电介质特性与测量",u"E070202绝缘与功能电介质材料的应用基础",u"E0703电机与电器",u"E070301电弧与电接触",u"E070302电器",u"E070303电机及其系统",u"E0704电力系统",u"E070401电力系统分析",u"E070402电力系统控制",u"E070403电力系统保护",u"E0705高电压与绝缘",u"E070501高电压与大电流",u"E070502电气设备绝缘",u"E070503过电压及其防护",u"E0706电力电子学",u"E070601电力电子器件及其应用",u"E070602电力电子系统及其控制",u"E0707脉冲功率技术",u"E0708气体放电与放电等离子体技术",u"E0709电磁环境与电磁兼容",u"E0710超导电工学",u"E0711生物电磁技术",u"E0712电能储存与节电技术",u"E08建筑环境与结构工程学科",u"E0801建筑学",u"E080101建筑设计与理论",u"E080102建筑历史与理论",u"E0802城乡规划",u"E080201城乡规划设计与理论",u"E080202风景园林规划设计与理论",u"E0803建筑物理",u"E080301建筑热环境",u"E080302建筑光环境",u"E080303建筑声环境",u"E0804环境工程",u"E080401给水处理",u"E080402污水处理与资源化",u"E080403城镇给排水系统",u"E080404城镇固体废弃物处置与资源化",u"E080405空气污染治理",u"E080406城市受污染水环境的工程修复",u"E0805结构工程",u"E080501混凝土结构与砌体结构",u"E080502钢结构与空间结构",u"E080503组合结构与混合结构",u"E080504新型结构与新材料结构",u"E080505桥梁工程",u"E080506地下工程与隧道工程",u"E080507结构分析、计算与设计理论",u"E080508结构实验方法与技术",u"E080509结构健康监测",u"E080510既有结构性能评价与修复",u"E080511混凝土结构材料",u"E080512土木工程施工与管理",u"E0806岩土与基础工程",u"E080601地基与基础工程",u"E080602岩土工程减灾",u"E080603环境岩土工程",u"E0807交通工程",u"E080701交通规划理论与方法",u"E080702交通环境工程",u"E080703道路工程",u"E080704铁道工程",u"E0808防灾工程",u"E080801地震工程",u"E080802风工程",u"E080803结构振动控制",u"E080804工程防火",u"E080805城市与生命线工程防灾",u"E09水利科学与海洋工程",u"E0901水文、水资源",u"E090101洪涝和干旱与减灾",u"E090102水文过程和模型及预报",u"E090103流域水循环与流域综合管理",u"E090104水资源分析与管理",u"E090105水资源开发与利用",u"E0902农业水利",u"E090201农业水循环与利用",u"E090202灌溉与排水",u"E090203灌排与农业生态环境",u"E0903水环境与生态水利",u"E090301水环境污染与修复",u"E090302农业非点源污染与劣质水利用",u"E090303水利工程对生态与环境的影响",u"E0904河流海岸动力学与泥沙研究",u"E090401泥沙运动力学",u"E090402流域泥沙运动过程",u"E090403河流泥沙及演变",u"E090404河口泥沙与演变",u"E090405工程泥沙",u"E0905水力学与水信息学",u"E090501工程水力学",u"E090502地下与渗流水力学",u"E090503地表与河道水力学",u"E090504水信息学与数字流域",u"E0906水力机械及其系统",u"E090601水力机械的流动理论",u"E090602空蚀和磨损及多相流",u"E090603电站和泵站系统",u"E090604监测和诊断及控制",u"E0907岩土力学与岩土工程",u"E090701岩土体本构关系与数值模拟",u"E090702岩土体试验、现场观测与分析",u"E090703软基与岩土体加固和处理",u"E090704岩土体渗流及环境效应",u"E090705岩土体应力变形及灾害",u"E0908水工结构和材料及施工",u"E090801水工结构动静力分析与控制",u"E090802水工结构实验、观测与分析",u"E090803水工和海工材料",u"E090804水工施工及管理",u"E0909海岸工程",u"E090901海岸工程的基础理论",u"E090902河口和海岸污染与治理",u"E090903港口航道及海岸建筑物",u"E090904海岸防灾与河口治理",u"E0910海洋工程",u"E091001海洋工程的基础理论",u"E091002船舶和水下航行器",u"E091003海洋建筑物与水下工程",u"E091004海上作业与海事保障",u"E091005海洋资源开发利用",u"F信息科学部",u"F01电子学与信息系统",u"F0101信息理论与信息系统",u"F010101信息论",u"F010102信源编码与信道编码",u"F010103通信网络与通信系统安全",u"F010104网络服务理论与技术",u"F010105信息系统建模与仿真",u"F010106认知无线电",u"F0102通信理论与系统",u"F010201网络通信理论与技术",u"F010202无线通信理论与技术",u"F010203空天通信理论与技术",u"F010204多媒体通信理论与技术",u"F010205光、量子通信理论与系统",u"F010206计算机通信理论与系统",u"F0103信号理论与信号处理",u"F010301多维信号处理",u"F010302声信号分析与处理",u"F010303雷达原理与技术",u"F010304雷达信号处理",u"F010305自适应信号处理",u"F010306人工神经网络",u"F0104信息处理方法与技术",u"F010401图像处理",u"F010402图像理解与识别",u"F010403多媒体信息处理",u"F010404探测与成像系统",u"F010405信息检测与估计",u"F010406智能信息处理",u"F010407视觉信息获取与处理",u"F010408遥感信息获取与处理",u"F010409网络信息获取与处理",u"F010410传感信息提取与处理",u"F0105电路与系统",u"F010501电路设计理论与技术",u"F010502电路故障检测理论与技术",u"F010503电路网络理论",u"F010504高性能电路",u"F010505非线性电路系统理论与应用",u"F010506功能集成电路与系统",u"F010507功率电子技术与系统",u"F010508射频技术与系统",u"F010509电路与系统可靠性",u"F0106电磁场与波",u"F010601电磁场理论",u"F010602计算电磁学",u"F010603散射与逆散射",u"F010604电波传播",u"F010605天线理论与技术",u"F010606毫米波与亚毫米波技术",u"F010607微波集成电路与元器件",u"F010608太赫兹电子技术",u"F010609微波光子学",u"F010610电磁兼容",u"F010611瞬态电磁场理论与应用",u"F010612新型介质电磁特性与应用",u"F0107物理电子学",u"F010701真空电子学",u"F010702量子、等离子体电子学",u"F010703超导电子学",u"F010704相对论电子学",u"F010705纳电子学",u"F010706表面和薄膜电子学",u"F010707新型电磁材料与器件基础研究",u"F010708分子电子学",u"F010709有机、无机电子学",u"F0108生物电子学与生物信息处理",u"F010801电磁场生物效应",u"F010802生物电磁信号检测与分析",u"F010803生物分子信息检测与识别",u"F010804生物细胞信号提取与分析",u"F010805生物信息处理与分析",u"F010806生物系统信息网络与分析",u"F010807生物系统功能建模与仿真",u"F010808仿生信息处理方法与技术",u"F010809系统生物学理论与技术",u"F010810医学信息检测方法与技术",u"F0109敏感电子学与传感器",u"F010901机械传感机理与信息检测",u"F010902气体、液体信息传感机理与检测",u"F010903压电、光电信息传感机理与检测",u"F010904生物信息传感机理与检测",u"F010905微纳米传感器原理与集成",u"F010906多功能传感器与综合技术",u"F010907新型敏感材料特性与器件",u"F010908新型传感器理论与技术",u"F010909传感信息融合与处理",u"F02计算机科学",u"F0201计算机科学的基础理论",u"F020101理论计算机科学",u"F020102新型计算模型",u"F020103计算机编码理论",u"F020104算法及其复杂性",u"F020105容错计算",u"F020106形式化方法",u"F020107机器智能基础理论与方法",u"F0202计算机软件",u"F020201软件理论与软件方法学",u"F020202软件工程",u"F020203程序设计语言及支撑环境",u"F020204数据库理论与系统",u"F020205系统软件",u"F020206并行与分布式软件",u"F020207实时与嵌入式软件",u"F020208可信软件",u"F0203计算机体系结构",u"F020301计算机系统建模与模拟",u"F020302计算机系统设计与性能评测",u"F020303计算机系统安全与评估",u"F020304并行与分布式处理",u"F020305高性能计算与超级计算机",u"F020306新型计算系统",u"F020307计算系统可靠性",u"F020308嵌入式系统",u"F0204计算机硬件技术",u"F020401测试与诊断技术",u"F020402数字电路功能设计与工具",u"F020403大容量存储设备与系统",u"F020404输入输出设备与系统",u"F020405高速数据传输技术",u"F0205计算机应用技术",u"F020501计算机图形学",u"F020502计算机图像与视频处理",u"F020503多媒体与虚拟现实技术",u"F020504生物信息计算",u"F020505科学工程计算与可视化",u"F020506人机界面技术",u"F020507计算机辅助技术",u"F020508模式识别理论及应用",u"F020509人工智能应用",u"F020510信息系统技术",u"F020511信息检索与评价",u"F020512知识发现与知识工程",u"F020513新应用领域中的基础研究",u"F0206自然语言理解与机器翻译",u"F020601计算语言学",u"F020602语法分析",u"F020603汉语及汉字信息处理",u"F020604少数民族语言文字信息处理",u"F020605机器翻译理论方法与技术",u"F020606自然语言处理相关技术",u"F0207信息安全",u"F020701密码学",u"F020702安全体系结构与协议",u"F020703信息隐藏",u"F020704信息对抗",u"F020705信息系统安全",u"F0208计算机网络",u"F020801计算机网络体系结构",u"F020802计算机网络通信协议",u"F020803网络资源共享与管理",u"F020804网络服务质量",u"F020805网络安全",u"F020806网络环境下的协同技术",u"F020807网络行为学与网络生态学",u"F020808移动网络计算",u"F020809传感网络协议与计算",u"F03自动化",u"F0301控制理论与方法",u"F030101线性与非线性系统控制",u"F030102过程与运动体控制",u"F030103网络化系统分析与控制",u"F030104离散事件动态系统控制",u"F030105混杂与多模态切换系统控制",u"F030106时滞系统控制",u"F030107随机与不确定系统控制",u"F030108分布参数系统控制",u"F030109采样与离散系统控制",u"F030110递阶与分布式系统控制",u"F030111量子与微纳系统控制",u"F030112生物生态系统的调节与控制",u"F030113最优控制",u"F030114自适应与学习控制",u"F030115鲁棒与预测控制",u"F030116智能与自主控制",u"F030117故障诊断与容错控制",u"F030118系统建模、分析与综合",u"F030119系统辨识与状态估计",u"F030120系统仿真与评估",u"F030121控制系统计算机辅助分析与设计",u"F0302系统科学与系统工程",u"F030201系统科学理论与方法",u"F030202系统工程理论与方法",u"F030203复杂系统及复杂网络理论与方法",u"F030204系统生物学中的复杂性分析与建模",u"F030205生物生态系统分析与计算机模拟",u"F030206社会经济系统分析与计算机模拟",u"F030207管理与决策支持系统的理论与技术",u"F030208管控一体化系统",u"F030209智能交通系统",u"F030210先进制造与产品设计",u"F030211系统安全与防护",u"F030212系统优化与调度",u"F030213系统可靠性理论",u"F0303导航、制导与传感技术",u"F030301导航、制导与测控",u"F030302被控量检测及传感器技术",u"F030303生物信息检测及传感器技术",u"F030304微弱信息检测与微纳传感器技术",u"F030305多相流检测及传感器技术",u"F030306软测量理论与方法",u"F030307传感器网络与多源信息融合",u"F030308多传感器集成系统",u"F0304模式识别",u"F030401模式识别基础",u"F030402特征提取与选择",u"F030403图像分析与理解",u"F030404语音识别、合成与理解",u"F030405文字识别",u"F030406生物特征识别",u"F030407生物分子识别",u"F030408目标识别与跟踪",u"F030409网络信息识别与理解",u"F030410机器视觉",u"F030411模式识别系统及应用",u"F0305人工智能与知识工程",u"F030501人工智能基础",u"F030502知识的表示、发现与获取",u"F030503本体论与知识库",u"F030504数据挖掘与机器学习",u"F030505逻辑、推理与问题求解",u"F030506神经网络基础及应用",u"F030507进化算法及应用",u"F030508智能Agent的理论与方法",u"F030509自然语言理解与生成",u"F030510智能搜索理论与算法",u"F030511人机交互与人机系统",u"F030512智能系统及应用",u"F0306机器人学及机器人技术",u"F030601机器人环境感知与路径规划",u"F030602机器人导航、定位与控制",u"F030603智能与自主机器人",u"F030604微型机器人与特种机器人",u"F030605仿生与动物型机器人",u"F030606多机器人系统与协调控制",u"F0307认知科学及智能信息处理",u"F030701知觉与注意信息的表达和整合",u"F030702学习与记忆过程的信息处理",u"F030703感知、思维与语言模型",u"F030704基于脑成像技术的认知功能",u"F030705基于认知机理的计算模型及应用",u"F030706脑机接口技术及应用",u"F030707群体智能的演化与自适应",u"F04半导体科学与信息器件",u"F0401半导体晶体与薄膜材料",u"F040101半导体晶体材料",u"F040102非晶、多晶和微纳晶半导体材料",u"F040103薄膜半导体材料",u"F040104半导体异质结构和低维结构材料",u"F040105SOI材料",u"F040106半导体材料工艺设备的设计与研究",u"F040107有机/无机半导体复合材料",u"F040108有机/聚合物半导体材料",u"F0402集成电路设计与测试",u"F040201系统芯片SoC设计方法与IP复用技术",u"F040202模拟/混合、射频集成电路设计",u"F040203超深亚微米集成电路低功耗设计",u"F040204集成电路设计自动化理论与CAD技术",u"F040205纳米尺度CMOS集成电路设计理论",u"F040206系统芯片SoC的验证与测试理论",u"F040207MEMS/MCM/生物芯片建模与模拟",u"F0403半导体光电子器件",u"F040301半导体发光器件",u"F040302半导体激光器",u"F040303半导体光探测器",u"F040304光集成和光电子集成",u"F040305半导体成像与显示器件",u"F040306半导体光伏材料与太阳电池",u"F040307基于柔性衬底的光电子器件与集成",u"F040308新型半导体光电子器件",u"F040309光电子器件封装与测试",u"F0404半导体电子器件",u"F040401半导体传感器",u"F040402半导体微波器件与集成",u"F040403半导体功率器件与集成",u"F040404半导体能量粒子探测器",u"F040405半导体电子器件工艺及封装技术",u"F040406薄膜电子器件与集成",u"F040407新型半导体电子器件",u"F0405半导体物理",u"F040501半导体材料物理",u"F040502半导体器件物理",u"F040503半导体表面与界面物理",u"F040504半导体中杂质与缺陷物理",u"F040505半导体输运过程与半导体能谱",u"F040506半导体低维结构物理",u"F040507半导体光电子学",u"F040508自旋学物理",u"F040509半导体中新的物理问题",u"F0406集成电路制造与封装",u"F040601集成电路制造中的工艺技术与相关材料",u"F040602GeSi/Si、SOI和应变Si等新结构集成电路",u"F040603抗辐射集成电路",u"F040604集成电路的可靠性与可制造性",u"F040605芯片制造专用设备研制中的关键技术",u"F040606先进封装技术与系统封装",u"F040607纳米电子器件及其集成技术",u"F0407半导体微纳机电器件与系统",u"F040701微纳机电系统模型、设计与EDA",u"F040702微纳机电系统工艺、封装、测试及可靠性",u"F040703微纳机电器件",u"F040704RF/微波微纳机电器件与系统",u"F040705微纳光机电器件与系统",u"F040706芯片微全分析系统",u"F0408新型信息器件",u"F040801纳米结构信息器件与纳电子技术",u"F040802基于分子结构的信息器件",u"F040803量子器件与自旋器件",u"F040804超导信息器件",u"F040805新原理信息器件",u"F05光学和光电子学",u"F0501光学信息获取与处理",u"F050101光学计算和光学逻辑",u"F050102光学信号处理与人工视觉",u"F050103光存贮材料、器件及技术",u"F050104光全息与数字全息技术",u"F050105光学成像、图像分析与处理",u"F050106光电子显示材料、器件及技术",u"F0502光子与光电子器件",u"F050201有源器件",u"F050202无源器件",u"F050203功能集成器件",u"F050204有机/聚合物光电子器件与光子器件",u"F050205光探测材料与器件",u"F050206紫外光电材料与器件",u"F050207光子晶体及器件",u"F050208光纤放大器与激光器",u"F050209发光器件与光源",u"F050210微纳光电子器件与光量子器件",u"F050211光波导器件",u"F050212新型光电子器件",u"F0503传输与交换光子学",u"F050301导波光学与光信息传输",u"F050302光通信与光网络关键技术与器件",u"F050303自由空间光传播与通信关键技术",u"F050304光学与光纤传感材料、器件及技术",u"F050305光纤材料及特种光纤",u"F050306测试技术",u"F050307光开关、光互连与光交换",u"F0504红外物理与技术",u"F050401红外物理",u"F050402红外辐射与物质相互作用",u"F050403红外探测、传输与发射",u"F050404红外探测材料与器件",u"F050405红外成像光谱和信息识别",u"F050406红外技术新应用",u"F050407红外遥感和红外空间技术",u"F050408太赫兹波技术及应用",u"F0505非线性光学与量子光学",u"F050501非线性光学效应及应用",u"F050502光学频率变换",u"F050503光量子计算、保密通讯与信息处理",u"F050504光学孤子与非线性传播",u"F050505强场与相对论的非线性光学",u"F0506激光",u"F050601激光物理",u"F050602激光与物质相互作用",u"F050603超快光子学与超快过程",u"F050604固体激光器件",u"F050605气体、准分子激光",u"F050606自由电子激光与X射线激光",u"F050607新型激光器件",u"F050608激光技术及应用",u"F0507光谱技术",u"F050701新型光谱分析法与设备",u"F050702光谱诊断技术",u"F050703超快光谱技术",u"F0508应用光学",u"F050801光学CAD与虚拟光学",u"F050802薄膜光学",u"F050803先进光学仪器",u"F050804先进光学制造与检测",u"F050805微小光学器件与系统",u"F050806光度学与色度学",u"F050807自适应光学及二元光学",u"F050808光学测量中的标准问题",u"F050809制造技术中的光学问题",u"F0509光学和光电子材料",u"F050901激光材料",u"F050902非线性光学材料",u"F050903功能光学材料",u"F050904有机/无机光学复合材料",u"F050905分子基光电子材料",u"F050906新光学材料",u"F0510空间光学",u"F051001空间光学遥感方法与成像仿真",u"F051002空间目标光学探测与识别",u"F051003深冷空间光学系统与深冷系统技术",u"F051004空间激光应用技术",u"F051005光学相控阵",u"F0511大气与海洋光学",u"F051101大气光学",u"F051102激光遥感与探测",u"F051103水色信息获取与处理",u"F051104水下目标、海底光学探测与信息处理",u"F051105海洋光学",u"F0512生物、医学光子学",u"F051201光学标记、探针与光学功能成像",u"F051202单分子操控与显微成像技术",u"F051203生命系统的光学效应及机理",u"F051204光与生物组织相互作用",u"F051205生物组织光谱技术及成像",u"F051206新型医学光学诊疗方法与仪器",u"F0513交叉学科中的光学问题",u"G管理科学部",u"G01管理科学与工程",u"G0101管理科学和管理思想史",u"G0102一般管理理论与研究方法论",u"G0103运筹与管理",u"G010301优化理论与方法",u"G010302排序、排队论与存储论",u"G010303供应链基础理论",u"G0104决策理论与方法",u"G0105对策理论与方法",u"G0106评价理论与方法",u"G0107预测理论与方法",u"G0108管理心理与行为",u"G0109管理系统工程",u"G010901管理系统分析",u"G010902管理系统仿真",u"G0110工业工程与管理",u"G0111系统可靠性与管理",u"G0112信息系统与管理",u"G011201管理信息系统",u"G011202决策支持系统",u"G011203管理信息与数据挖掘",u"G0113数量经济理论与方法",u"G0114风险管理技术与方法",u"G0115金融工程",u"G0116管理复杂性研究",u"G0117知识管理",u"G0118工程管理",u"G02工商管理",u"G0201战略管理",u"G020101战略理论与决策",u"G020102竞争力与竞争优势",u"G020103战略制定、实施与评价",u"G0202企业理论",u"G0203创新管理",u"G0204组织行为与组织文化",u"G020401组织行为",u"G020402组织文化与跨文化管理",u"G0205人力资源管理",u"G020501领导理论",u"G020502薪酬与绩效管理",u"G020503人力资源开发",u"G0206公司理财与财务管理",u"G0207会计与审计",u"G020701会计理论与方法",u"G020702审计理论与方法",u"G0208市场营销",u"G020801市场营销理论与方法",u"G020802品牌与消费行为",u"G020803网络营销",u"G0209运作管理",u"G020901生产管理",u"G020902质量管理",u"G0210技术管理与技术经济",u"G021001企业研发与技术创新",u"G021002企业知识产权管理",u"G0211企业信息管理",u"G021101企业信息资源管理",u"G021102电子商务与商务智能",u"G0212物流与供应链管理",u"G0213项目管理",u"G0214服务管理",u"G0215创业与中小企业管理",u"G021501创业管理",u"G021502中小企业管理",u"G0216非营利组织管理",u"G03宏观管理与政策",u"G0301宏观经济管理与战略",u"G0302金融管理与政策",u"G030201银行体系与货币政策",u"G030202资本市场管理",u"G0303财税管理与政策",u"G0304产业政策与管理",u"G0305农林经济管理",u"G030501林业经济管理",u"G030502农业产业管理",u"G030503农村发展与管理",u"G030504农户及组织管理",u"G0306公共管理与公共政策",u"G030601公共管理基础理论",u"G030602公共政策分析",u"G030603政府管理",u"G030604社会管理与服务",u"G0307科技管理与政策",u"G030701科学计量学与科技评价",u"G030702科研管理",u"G030703科技创新管理",u"G030704知识产权管理与宏观政策",u"G0308卫生管理与政策",u"G0309教育管理与政策",u"G0310公共安全与危机管理",u"G0311劳动就业与社会保障",u"G031101劳动就业管理",u"G031102社会保障管理",u"G0312资源环境政策与管理",u"G031201可持续发展管理",u"G031202环境政策与生态管理",u"G031203资源管理与政策",u"G0313区域发展管理",u"G031301区域发展战略管理",u"G031302城镇发展与管理",u"G0314信息资源管理",u"G031401图书情报档案管理",u"G031402政府与社会信息资源管理",u"H医学科学部",u"H01呼吸系统",u"H0101肺及气道结构、功能与发育异常",u"H0102呼吸系统遗传性疾病",u"H0103呼吸调控异常",u"H0104呼吸系统炎症与感染",u"H0105呼吸系统免疫性疾病及变应性肺疾病",u"H0106气道重塑与气道疾病",u"H0107支气管哮喘",u"H0108慢性阻塞性肺疾病",u"H0109肺循环及肺血管疾病",u"H0110间质性肺疾病",u"H0111急性肺损和急性呼吸窘迫综合征",u"H0112呼吸袞竭与呼吸支持",u"H0113睡眠呼吸障碍",u"H0114纵隔与胸膜疾病",u"H0115胸廊/膈肌结构、功能及发育异常",u"H0116肺移植和肺保护",u"H0117呼吸系统疾病诊疗新技术",u"H0118呼吸系统疾病其他科学问题",u"H02循环系统",u"H0201心脏结构与功能异常",u"H0202循环系统遗传性疾病",u"H0203心肌细胞/血管细胞损伤、修复、重构和再生",u"H0204心脏发育异常与先天性心脏病",u"H0205心电活动异常与心律失常",u"H0206冠状动脉性心脏病",u"H0207肺源性心脏病",u"H0208心肌炎和心肌病",u"H0209感染性心内膜炎",u"H0210心脏瓣膜疾病",u"H0211心包疾病",u"H0212心力衰竭",u"H0213心脏/血管移植和辅助循环",u"H0214血压调节异常与高血压病",u"H0215动脉粥样硬化与动脉硬化",u"H0216主动脉疾病",u"H0217周围血管疾病",u"H0218淋巴管与淋巴循环疾病",u"H0219微循环与休克",u"H0220血管发生异常及血管结构与功能异常",u"H0221循环系统免疫相关疾病",u"H0222循环系统疾病诊疗新技术",u"H0223循环系统疾病其他科学问题",u"H03消化系统",u"H0301消化系统发育异常",u"H0302消化系统遗传性疾病",u"H0303消化道结构与功能异常",u"H0304肝胆胰结构与功能异常",u"H0305腹壁/腹膜结构及功能异常",u"H0306消化道内环境紊乱、黏膜屏障障碍及相关疾病",u"H0307消化道动力异常及功能性胃肠病",u"H0308消化系统内分泌及神经体液调节异常",u"H0309胃酸分泌异常及酸相关性疾病",u"H0310胃肠道免疫相关疾病",u"H0311消化系统血管及循环障碍性疾病",u"H0312胃肠道及腹腔感染性疾病",u"H0313肝胆胰免疫及相关疾病",u"H0314肝脏代谢陣碍及相关疾病",u"H0315药物、毒物及酒精性消化系统疾病",u"H0316炎性及感染性肝病",u"H0317肝纤维化、肝硬化与门脉高压症",u"H0318肝再生、肝保护、肝袞竭、人工肝",u"H0319胆石成因、胆石症及胆道系统炎症",u"H0320胰腺外分泌功能异常与胰腺炎",u"H0321消化系统器官移植",u"H0322消化系统疾病诊疗新技术",u"H0323消化系统疾病其他科学问题",u"H04生殖系统/围生医学/新生儿",u"H0401女性生殖系统结构、功能与发育异常",u"H0402女性生殖系统损伤与修复",u"H0403女性生殖系统炎症与感染",u"H0404女性生殖内分泌异常及相关疾病",u"H0405女性生殖系统遗传性疾病",u"H0406子宫内膜异位症与子宫腺肌症",u"H0407女性盆底功能降碍",u"H0408女性性功能降碍",u"H0409乳腺结构、功能及发育异常",u"H0410男性生殖系统结构、功能与发育异常",u"H0411男性生殖系统损伤与修复",u"H0412男性生殖系统炎症与感染",u"H0413男性生殖内分泌异常及相关疾病",u"H0414男性生殖系统遗传性疾病",u"H0415男性性功能障碍",u"H0416卵子发生与受精异常",u"H0417胚胎着床及早期胚胎发育异常",u"H0418胎盘结构与功能异常",u"H0419胎儿发育与产前诊断",u"H0420妊娠及妊娠相关性疾病",u"H0421分娩与产褥",u"H0422新生儿相关疾病",u"H0423避孕、节育与妊娠终止",u"H0424精子发生异常与男性不育",u"H0425女性不孕不育与辅助生殖",u"H0426生殖医学工程",u"H0427生殖免疫相关疾病",u"H0428生殖系统移植",u"H0429生殖系统/围生医学/新生儿疾病相关诊疗新技术",u"H0430生殖系统/围生医学/新生儿疾病其他科学问题",u"H05泌尿系统",u"H0501泌尿系统结构、功能与发育异常",u"H0502泌尿系统遗传性疾病",u"H0503泌尿系统损伤与修复",u"H0504泌尿系统感染",u"H0505泌尿系统免疫相关疾病",u"H0506泌尿系统结石",u"H0507肾脏物质转运异常",u"H0508肾脏内分泌功能异常",u"H0509原发性肾脏疾病",u"H0510继发性肾脏疾病",u"H0511肾衰竭",u"H0512肾移植",u"H0513前列腺疾病",u"H0514膀胱疾病",u"H0515尿动力学",u"H0516血液净化和替代治疗",u"H0517泌尿系统疾病诊疗新技术",u"H0518泌尿系统疾病其他科学问题",u"H06运动系统",u"H0601运动系统结构、功能和发育异常",u"H0602运动系统遗传性疾病",u"H0603运动系统免疫相关疾病",u"H0604骨、关节、软组织医用材料",u"H0605骨、关节、软组织损伤与修复",u"H0606骨、关节、软组织移植与重建",u"H0607骨、关节、软组织感染",u"H0608骨、关节、软组织疲劳与恢复",u"H0609骨、关节、软组织退行性病变",u"H0610骨、关节、软组织运动损伤",u"H0611运动系统崎形与矫正",u"H0612运动系统疾病诊疗新技术",u"H0613运动系统疾病其他科学问题",u"H07内分泌系统/代谢和营养支持",u"H0701松果体/下丘脑/垂体发育及结构异常",u"H0702甲状腺/甲状旁腺发育及结构异常",u"H0703肾上腺发育及结构异常",u"H0704胰岛发育、胰岛细胞分化再生及功能调控异常与胰岛移植",u"H0705内分泌系统炎症与感染",u"H0706内分泌系统遗传性疾病",u"H0707内分泌系统免疫相关疾病",u"H0708松果体/下丘脑/垂体疾病及功能异常",u"H0709甲状腺/甲状旁腺疾病及功能异常",u"H0710肾上腺疾病及功能异常",u"H0711糖尿病发生的遗传和环境因素",u"H0712血糖调控异常与胰岛素抵抗",u"H0713糖尿病",u"H0714其他组织的内分泌功能异常",u"H0715甲状腺和甲状旁腺移植",u"H0716能里代谢调节异常及肥胖",u"H0717代谢综合征",u"H0718糖代谢异常",u"H0719脂代谢异常",u"H0720脂肪细胞分化及功能异常",u"H0721氨基酸代谢异常",u"H0722核酸代谢异常",u"H0723水、电解质代谢障碍及酸碱平衡异常",u"H0724微置元紊、维生索代谢异常",u"H0725钙磷代谢异常",u"H0726骨转换、骨代谢异常和骨质疏松",u"H0727营养不良与营养支持",u"H0728遗传性代谢缺陷",u"H0729内分泌系统疾病/代谢异常与营养支持领域相关新技术",u"H0730内分泌系统疾病/代谢异常与营养支持其他科学问题",u"H08血液系统",u"H0801造血、造血调控与造血微环境异常",u"H0802造血相关器官结构及功能异常",u"H0803红细胞异常及相关疾病",u"H0804白细胞异常及相关疾病",u"H0805血小板异常及相关疾病",u"H0806再生障碍性贫血和骨髄衰竭",u"H0807骨髄增生异常综合征",u"H0808骨髓培殖性疾病",u"H0809血液系统免疫相关疾病",u"H0810血液系统感染性疾病",u"H0811出血、凝血与血栓",u"H0812白血病",u"H0813造血干细胞移植及并发症",u"H0814血型与输血",u"H0815遗传性血液病",u"H0816血液系统疾病诊疗新技术",u"H0817血液系统疾病其他科学问题",u"H0818淋巴瘤及其他淋巴增殖性疾病",u"H0819骨髓瘤及其他浆细胞疾病",u"H09神经系统和精神疾病",u"H0901意识障碍",u"H0902认知功能障碍",u"H0903躯体感觉、疼痛与镇痛",u"H0904运动调节与运动障碍",u"H0905神经发育、遗传、代谢相关疾病",u"H0906脑血管结构、功能异常及相关疾病",u"H0907神经免疫调节异常及神经免疫相关疾病",u"H0908神经系统屏降和脑禅液异常及相关疾病",u"H0909神经系统炎症及感染性疾病",u"H0910脑'脊翻'周围神经损伤及修复",u"H0911周围神经、神经肌肉接头、肌肉、自主神经疾病",u"H0912神经变性、再生及相关疾病",u"H0913神经电活动异常与发作性疾病",u"H0914脑功能保护、治疗与康复",u"H0915节律调控与节律紊乱",u"H0916睡眠与睡眠障碍",u"H0917器质性粞神疾病",u"H0918物质依赖和其他成瘾性障碍",u"H0919精神分裂症和其他精神障碍",u"H0920神经症和应激相关障碍",u"H0921心境障碍、心理生理障碍和心身疾病",u"H0922人格障碍、冲动控制障碍和性心理异常",u"H0923儿童和青少年精神障碍",u"H0924其他精神陣碍与精神卫生问题",u"H0925精神疾病的心理测爱和评估",u"H0926心理咨询与心理治疗",u"H0927危机干预",u"H0928神经系统和精神疾病诊疗新技术",u"H0929神经系统和精神疾病其他科学问题",u"H10医学免疫学",u"H1001免疫器官/组织/细胞的发育分化异常",u"H1002免疫应答异常",u"H1003免疫反应相关因子与疾病",u"H1004免疫识别/免疫耐受/免疫调节异常",u"H1005炎症、感染与免疫",u"H1006器官移植与移植免疫",u"H10G7超敏反应性疾病",u"H1008自身免疫性疾病",u"H1009继发及原发性免疫缺陷性疾病",u"H1010固有免疫异常",u"H1011神经内分泌免疫异常",u"H1012黏膜免疫疾病",u"Hl013疾病的系统免疫学",u"H1014疫苗和佐剂研究艘种/免疫防治",u"H1015免疫相关疾病诊疗新技术",u"H1016免疫相关疾病其他科学问题",u"H11皮肤及其附属器",u"H1101皮肤形态、结构和功能异常",u"H1102皮肤遗传及相关疾病",u"H1103皮肤免疫性疾病",u"H1104皮肤感染",u"H1105非感染性皮肤病",u"H1106皮肤附厲器及相关疾病",u"H1107皮肤及其附厲器疾病诊疗新技术",u"H1108皮肤及其附属器疾病其他科学问题",u"H12眼科学",u"H1201角膜及眼表疾病",u"H1202晶状体与白内障",u"H1203巩膜、葡萄膜、眼免疫",u"H1204胬光眼、视神经及视路相关疾病",u"H1205视网膜、脉络膜及玻璃体相关疾病",u"H1206视觉、视光学与近视、弱视及眼肌疾病",u"H1207全身疾病眼部表现、眼眶疾病",u"H1208眼遗传性疾病",u"H1209眼组织移植",u"H1210眼科疾病诊疗新技术",u"H1211眼科疾病其他科学问题",u"H13耳鼻咽喉头颈科学",u"H1301嗅觉、鼻及前频底疾病",u"H1302咽喉及颈部疾病",u"H1303耳及侧颅底疾病",u"H1304听觉异常与平衡障碍",u"H1305耳鼻咽喉遗传与发育相关疾病",u"H1306耳鼻咽喉疾病诊疗新技术",u"H1307耳鼻咽喉疾病其他科学问题",u"H14口腔颅颔面科学",u"H1401口腔颅颌面组织生长发育及牙再生",u"H1402颅颌面部骨、软骨组织的研究",u"H1403口腔颌面部遗传性疾病和发育畸形及软组织缺损修复",u"H1404牙体牙髋及根尖周组织疾病",u"H1405牙周及口腔黏膜疾病",u"H1406睡液、涎腺疾病、口腔颌面脉管神经及颌骨良性疾病",u"H1407味觉、口颌面疼痛、晈合及颞下颌关节疾病",u"H1408牙缺损、缺失及牙颌畸形的修复与矫治",u"H1409口腔颌面组织生物力学和生物材料",u"H1410口腔颌面疾病珍疗新技术",u"H1411口腔颌面疾病其他科学问题",u"H15急重症医学/创伤/烧伤/整形",u"H1501心肺复苏",u"H1502多脏器衰竭",u"H1503中毒",u"H1504创伤",u"H1505烧伤",u"H1506冻伤",u"H1507创面愈合与瘢痕",u"H1508体表组织器官畸形、损伤与修复、再生",u"H15的体表组织器官移植与再造",u"H1510颅颌面畸形与矫正",u"H1511急重症医学/创伤/烧伤/整形其他科学问题",u"H16肿瘤学",u"H1601肿瘤病因",u"H1602肿瘤发生",u"H1603肿瘤遗传与表观遗传",u"H1604肿瘤免疫",u"H1605肿瘤预防",u"H1606肿瘤复发与转移",u"H1607肿痛干细胞",u"H1608肿瘤诊断",u"H1609肿瘤化学药物治疗",u"H1610肿瘤物理治疗",u"H1611肿瘤生物治疗",u"H1612肿瘤综合治疗",u"H1613肿瘤康复（包括社会心理康复）",u"H1614肿瘤研究体系新技术",u"H161S呼吸系统肿瘤",u"H1617消化系统胂瘤",u"H1618神经系统肿瘤（含特殊感受器肿瘤）",u"H1619泌尿系统肿瘤",u"H1620男性生殖系统肿瘤",u"H1621女性生殖系统肿瘤",u"H1622乳腺肿瘤",u"H1623内分泌系统肿瘤",u"H1624骨与软组织肿瘤",u"H1625头颈部及颌面肿瘤",u"H1626皮肤、体表及其他部位肿瘤",u"H17康复医学",u"H1701康复医学",u"H18影像医学与生物医学工程",u"H1801磁共振结构成像与疾病诊断",u"H1802fMRI与脑、脊髄功能异常检测",u"H1803磁共振成像技术与造影剂",u"H1804X射线与CT、电子与离子束、放射诊断与质虽控制",u"H1805医学超声与声学造彩剂",u"H1806核医学",u"H1807医学光子学、光谱与光学成像",u"H1808分子彩像与分子探针",u"H1809医学图像数据处理与分析",u"H1810脑电图、脑磁图与脑机交互",u"H1811人体医学倍号检测、识别、处理与分析",u"H1812生物医学传感",u"H18L5生物医学系统建模及仿真",u"H1814医学信息系统与远程医疗",u"H1815治疗计划、导航与机器人辅助",u"H1816介入医学与工程",u"H1817康复工程与智能控制",u"H1818药物、基因载体系统",u"H1819纳米医学",u"H1820医用生物材料与植入科学",u"H1821细胞移植、组织再生与生物反应器",u"H1822组织工程与再生医学",u"H1823人工器官与特殊感受器仿生医学",u"H1824电磁与物理治疗",u"H1825用于检测、分析、成像及治疗的医学器件和仪器",u"H1826彩像医学与生物医学工程其他科学问题",u"H19医学病原生物与感染",u"H1901病原细菌'细菌感染与宿主免疫",u"H1902病原放线菌、放线菌感染与宿主免疫",u"H1903病原真菌、真菌感染与宿主免疫",u"H1904病毒、病毒感染与宿主免疫",u"H1905其他病原微生物及感染与宿主免疫",u"H1906寄生虫、寄生虫感染与宿主免疫",u"H1907传染病媒介生物",u"H1908病原生物变异与耐药",u"H1909医院获得性感染",u"H1910性传播疾病",u"H1911病原生物与感染研究与诊疗新技术",u"H1912病原生物与感染其他科学问题",u"H20检验医学",u"H2001临床生物化学检验",u"H2002临床微生物学检验",u"H2003临床细胞学和血液学检验",u"H2004临床免疫学检验",u"H2005临床分子生物学检验",u"H2006临床检验新技术",u"H2007检验医学其他科学问题",u"H21特种医学",u"H2101特种医学（航空、航天、航海、潜水、高原、极地等极端环境）",u"H22放射医学",u"H2201放射医学",u"H23法医学",u"H2301法医毒理、病理及毒物分析",u"H2302法医物证学、法医人类学",u"H2303法医精神病学及法医临床学",u"H2304法医学其他科学问题",u"H24地方病学/职业病学",u"H2401地方病学",u"H2402职业病学",u"H25老年医学",u"H2501老年医学",u"H26预防医学",u"H2601环境卫生",u"H2602职业卫生",u"H2603人类营荞",u"H2604食品卫生",u"H2605妇幼保健",u"H2606儿童少年卫生",u"H2607卫生毒理",u"H2608卫生分析化学",u"H2609传染病流行病学",u"H2610非传染病流行病学",u"H2611流行病学方法与卫生统计",u"H2612预防医学其他科学问题",u"H27中医学",u"H2701脏腑气血津液体质",u"H2702病因病机",u"H2703证候基础",u"H2704治则与治法",u"H2705中医方剂",u"H2706中医诊断",u"H2707经络与腧穴",u"H2708中医内科",u"H2709中医外科",u"H2710中医骨伤科",u"H2711中医妇科",u"H2712中医儿科",u"H2713中医眼科",u"H2714中医耳鼻喉科",u"H2715中医口腔科",u"H2716中医老年病",u"H2717中医养生与康复",u"H2718中医针灸",u"H2719按庠推拿",u"H2720民族医学",u"H2721中医学其他科学问题",u"H28中药学",u"H2801中药资源",u"H2802中药鉴定",u"H2803中药药效物质",u"H2804中药质里评价",u"H2805中药炮制",u"H2806中药制剂",u"H2807中药药性理论",u"H2808中药神经精神药理",u"H2809中药心脑血管药理",u"H2810中药抗肿瘤药理",u"H2811中药内分泌及代谢药理",u"H2812中药抗炎与免疫药理",u"H2813中药抗病毒与感染药理",u"H2814中药消化与呼吸药理",u"H2815中药泌尿与生殖药理",u"H2816中药药代动力学",u"H2817中药毒理",u"H2818民族药学",u"H2819中药学其他科学问题",u"H29中西医结合",u"H2901中西医结合基础理论",u"H2902中西医结合临床基础",u"H2903中医药学研究新技术和新方法",u"H30药物学",u"H3001合成药物化学",u"H3002天然药物化学",u"H30O3微生物药物",u"H3004生物技术药物",u"H3005海洋药物",u"H3006特种药物",u"H3007药物设计与药物信息",u"H3008药剂学",u"H3009药物材料",u"H3010药物分析",u"H3011药物资源",u"H3012药物学其他科学问题药理学",u"H3101神经精神药物药理",u"H3102心脑血笸药物药理",u"H3103老年病药物药理",u"H3104抗炎与免疫药物药理",u"H3105抗肿瘤药物药理",u"H3106抗感染药物药理",u"H3107代谢性疾病药物药理",u"H3108消化与呼吸系统药物药理",u"H3109血液、泌尿与生殖系统药物药理",u"H3110药物代谢与药物动力学",u"H3111临床药理",u"H3112药物毒理",u"H3113药理学其他科学问题",],
 }

FIRST_TAGS = [(k, k) for k in DOMAIN]
SECOND_TAGS = [(k, [
      [v, v] for v in val
     ]) for k, val in DOMAIN.items()]

class ExpertDomain(models.Model):
    domainserial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    domaintype = models.CharField(max_length=32, choices=FIRST_TAGS, verbose_name=u"*领域分类", help_text=u"研究领域所属分类",blank=True)
    domainname = models.CharField(max_length=32, choices=SECOND_TAGS, verbose_name=u"*学科名称", help_text=u"在该研究领域研究的学科名称", blank=True)
    domainkeywords = models.CharField(max_length=256, verbose_name=u"*中文关键字", help_text=u"中文关键字，若有多个请用空格分开", blank=True)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)

#工作履历 -- Step 11
class FormalJob(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    formaljob_serial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    formaljob_start = models.DateField(verbose_name=u"*起始时间", help_text=u"起始时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", blank=True)
    formaljob_end = models.DateField(verbose_name=u"结束时间", help_text=u"填写结束时间，或者至今；至今则留空。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    formaljob_country = models.CharField(max_length=32, verbose_name=u"*国家", choices=COUNTRY_CHOICE, default="CHN", help_text=u"工作地点所属国家", blank=True)
    formaljob_danwei = models.CharField(max_length=64, verbose_name=u"*工作单位", help_text=u"工作单位名称", blank=True)
    formaljob_zhiwu = models.CharField(max_length=64, verbose_name=u"*职务", help_text=u"担任之职务", blank=True)
    formaljob_zhiwujibie = models.CharField(max_length=64, verbose_name=u"职务级别", help_text=u"该职务所属的级别", null=True, blank=True)
    formaljob_zhichen = models.CharField(max_length=64, verbose_name=u"职称", help_text=u"职称", null=True, blank=True)
    formaljob_yanjiufangxiang = models.CharField(max_length=64, verbose_name=u"*研究方向", help_text=u"研究方向", blank=True)
    formaljob_gongzuoneirong = models.TextField(max_length=4096, verbose_name=u"*工作内容", help_text=u"工作内容描述（限500字）", blank=True)
    formaljob_gongzuoxingzhi = models.CharField(max_length=64, verbose_name=u"*工作性质", help_text=u"工作性质", null=True, blank=True)


#教育信息 -- Step 12
class Education(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    education_serial = models.IntegerField(verbose_name=u"序号", help_text=u"序号", blank=True)
    education_start = models.DateField(verbose_name=u"*起始时间", help_text=u"起始时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", blank=True)
    education_end = models.DateField(verbose_name=u"结束时间", help_text=u"填写结束时间，或者至今；至今则留空。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    education_country = models.CharField(max_length=32, verbose_name=u"国家", choices=COUNTRY_CHOICE, default="CHN", help_text=u"接受教育院校所属国家", blank=True)
    education_yuanxiaomingcheng = models.CharField(max_length=64, verbose_name=u"院校名称", help_text=u"院校名称", blank=True)
    education_zhuanye = models.CharField(max_length=64, verbose_name=u"专业", help_text=u"专业名称", blank=True)
    education_xueli = models.CharField(max_length=64, choices=XUELI_CHOICE, verbose_name=u"学历", help_text=u"所取得的学历，若未取得学历，请留空。例如：博士研究生", null=True, blank=True)
    education_xuewei = models.CharField(max_length=64, choices=XUEWEI_CHOICE, verbose_name=u"学位", help_text=u"所取得的学位，若未取得学位，请留空。例如：博士", null=True, blank=True)
    education_peixunjinxiu = models.CharField(max_length=64, verbose_name=u"培训进修", help_text=u"培训进修经历", null=True, blank=True)
    education_zhidaojiaoshi = models.CharField(max_length=32, verbose_name=u"指导教师", help_text=u"指导教师姓名，若无情留空", null=True, blank=True)


#学术兼职信息 -- Step 13
class PartTimeJob(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    parttimejob_serial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    parttimejob_start = models.DateField(verbose_name=u"*起始时间", help_text=u"起始时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", blank=True)
    parttimejob_end = models.DateField(verbose_name=u"结束时间", help_text=u"填写结束时间，或者至今；至今则留空。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    parttimejob_danwei = models.CharField(max_length=64, verbose_name=u"*兼职单位", help_text=u"学术兼职单位名称", blank=True)
    parttimejob_zhiwu = models.CharField(max_length=64, verbose_name=u"*职务", help_text=u"担任之职务", blank=True)
    parttimejob_sessionid = models.CharField(max_length=32, verbose_name=u"届次", help_text=u"此次学术兼职活动所属届次，如没有请留空", null=True, blank=True)


#学术评审信息 -- Step 14
class ReviewHistory(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    reviewhistory_serial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    reviewhistory_start = models.DateField(verbose_name=u"*起始时间", help_text=u"起始时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", blank=True)
    reviewhistory_end = models.DateField(verbose_name=u"结束时间", help_text=u"填写结束时间，或者至今；至今则留空。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    reviewhistory_content = models.TextField(max_length=4096, verbose_name=u"*评审内容", help_text=u"评审内容简介", blank=True)
    reviewhistory_weituojigou = models.CharField(max_length=64, verbose_name=u"*评审委托机构", help_text=u"评审委托机构", blank=True)


#承担项目情况 -- Step 15
class XiangmuInfo(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    xiangmuinfo_serial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    xiangmuinfo_name = models.CharField(max_length=256, verbose_name=u"*项目名称", help_text=u"项目名称", blank=True)
    xiangmuinfo_jibie = models.CharField(max_length=64, verbose_name=u"项目级别", help_text=u"项目级别", null=True, blank=True)
    xiangmuinfo_paiming = models.CharField(max_length=64, verbose_name=u"本人排名", help_text=u"本人排名", null=True, blank=True)
    xiangmuinfo_bianhao = models.CharField(max_length=256, verbose_name=u"项目编号", help_text=u"项目编号", null=True, blank=True)
    xiangmuinfo_zizhuleibie = models.CharField(max_length=256, verbose_name=u"资助类别", help_text=u"资助类别", null=True, blank=True)
    xiangmuinfo_jingfei = models.DecimalField(max_digits=31, decimal_places=6, verbose_name=u"*项目经费(万元)", help_text=u"项目经费(万元)", blank=True)
    xiangmuinfo_start = models.DateField(verbose_name=u"*起始时间", help_text=u"起始时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", blank=True)
    xiangmuinfo_end = models.DateField(verbose_name=u"结束时间", help_text=u"填写结束时间，或者至今；至今则留空。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)

#附件 -- Step 16
class Attachment(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    attachment_serial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    attachment_name = models.CharField(max_length=256, verbose_name=u"附件名称", help_text=u"附件名称（默认与上传附件文件名一致）", blank=True)
    attachment_type = models.CharField(max_length=64, verbose_name=u"*附件类型", help_text=u"附件类型描述", blank=True)
    attachment_file = models.FileField(upload_to=attachment_directory_path, verbose_name=u"附件", help_text=u"上传附件", blank=True)

class Project(models.Model):
    projectname = models.CharField(max_length=256, verbose_name=u"项目名称", help_text=u"项目名称")
    serial_no = models.CharField(max_length=64, verbose_name=u"项目编号", help_text=u"项目编号")
    shenbaodanwei = models.CharField(max_length=256, verbose_name=u"项目申报单位", help_text=u"项目申报单位")
    shenbaoriqi = models.DateField(verbose_name=u"项目申报日期", help_text=u"项目申报日期，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    leibie = models.CharField(max_length=64, verbose_name=u"项目类别", help_text=u"项目类别", null=True, blank=True)
    fuzeren = models.CharField(max_length=64, verbose_name=u"项目负责人", help_text=u"项目负责人", null=True, blank=True)
    fuzeren_dianhua = models.CharField(max_length=64, verbose_name=u"项目负责人电话", help_text=u"项目负责人电话", null=True, blank=True)
    yewuchushi = models.CharField(max_length=128, verbose_name=u"业务处室", help_text=u"业务处室", null=True, blank=True)
    yewuchushi_dianhua = models.CharField(max_length=64, verbose_name=u"业务处室电话", help_text=u"业务处室电话", null=True, blank=True)
    pingshengshijian = models.DateField(verbose_name=u"项目评审或验收时间", help_text=u"项目评审时间，或项目验收时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    yanshoushijian = models.DateField(verbose_name=u"项目验收时间", help_text=u"项目验收时间，精确到日。日期格式：YYYY-MM-DD；例如：1998-01-31", null=True, blank=True)
    pingshengdidian = models.CharField(max_length=128, verbose_name=u"项目评审或验收地点", help_text=u"项目评审地点，或项目验收地点", null=True, blank=True)
    yanshoudidian = models.CharField(max_length=128, verbose_name=u"项目验收地点", help_text=u"项目验收地点", null=True, blank=True)
    chouqurenshu = models.IntegerField(verbose_name=u"抽取人数", help_text=u"抽取评审专家人数", null=True, blank=True)
    chouquyaoqiu = models.TextField(max_length=4096, verbose_name=u"*抽取专家要求", help_text=u"抽取专家要求", null=True)
    startreviewdescription = models.TextField(max_length=4096, verbose_name=u"*项目评审说明", help_text=u"项目评审启动说明", null=True)
    state = models.CharField(max_length=32, verbose_name=u"状态")
    current_bindrec = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)
    started_at = models.DateField(verbose_name=u"项目评审启动时间", help_text=u"项目评审启动时间，默认为今日", null=True)
    finished_at = models.DateField(verbose_name=u"项目评审结束时间", help_text=u"项目评审结束时间，默认为今日", null=True)
    reviewers = models.ManyToManyField(
        Expert, 
        through='Reviewer',
        through_fields=('project', 'expert'),
    )

class Reviewer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=REVIEWER_STATE_CHOICE, default=REVIEWER_INITIAL, verbose_name=u"状态")
    isPrioritized = models.BooleanField(default=False, verbose_name=u"是否优先抽取", help_text=u"是否优先抽取")
    isnotified = models.BooleanField(default=False, verbose_name=u"是否已被通知", help_text=u"是否已被通知")
    comments = models.TextField(max_length=65536, verbose_name=u"评审内容", help_text=u"专家评审内容", null=True, blank=True)
    comments_attachments = models.FileField(upload_to=review_attachment_directory_path, verbose_name=u"评审附件", help_text=u"上传评审附件，多个附件请打包后上传", null=True, blank=True)
    #comments_committed = models.BooleanField(default=False, verbose_name=u"评审内容是否已提交", help_text=u"是否已经提交评审内容")
    review_state = models.CharField(max_length=2, default=REVIEW_STATE_NOTSTART, verbose_name=u"评审状态", help_text=u"该专家对项目评审的状态", null=True, blank=True)
    comments_on_comments = models.TextField(max_length=65536, verbose_name=u"评审评价", help_text=u"对专家评审质量之评价、评论", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)
    selected_at = models.DateTimeField(auto_now_add=False, null=True)

class BindRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    conditions = models.CharField(max_length=1024, verbose_name=u"Bind Conditions", help_text=u"Json Object For Python internal usage", null=True)
    bind_number = models.IntegerField(verbose_name=u"抽取人数", help_text=u"抽取评审专家人数", null=True, blank=True)
    candidate_number = models.IntegerField(verbose_name=u"匹配人数", help_text=u"匹配人数", null=True, blank=True)
    reviewer_number = models.IntegerField(verbose_name=u"实际抽取人数", help_text=u"实际抽取人数", null=True, blank=True)
    bind_comments = models.TextField(max_length=65536, verbose_name=u"抽取说明", help_text=u"抽取说明", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    binded_at = models.DateTimeField(null=True)
    rebinded_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)


