# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models

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

DOMAIN = (
    (u"国家科技部领域",(
        (u"数学", u"数学"),
        (u"信息科学与系统科学", u"信息科学与系统科学"),
        (u"物理学", u"物理学"),
        )
     ),
    (u"国家基金委领域", (
        (u"数理科学", u"数理科学"),
        (u"化学科学", u"化学科学"),
        (u"生命科学", u"生命科学"),
     )
)

#研究领域 -- Step 10
class ExpertDomain(models.Model):
    domainserial = models.IntegerField(verbose_name=u"*序号", help_text=u"序号", blank=True)
    domaintype = models.CharField(max_length=32, choices=DOMAIN, verbose_name=u"*领域分类", help_text=u"研究领域所属分类",blank=True)
    domainname = models.CharField(max_length=32, choices=domaintype.get_domaintype_display(), verbose_name=u"*学科名称", help_text=u"在该研究领域研究的学科名称", blank=True)
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

