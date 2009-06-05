# -*- coding: utf-8 -*-

from esus.phorum.models import Category

def create_zena_categories(case, commit=True):
    # nested Czech category
    case.category_cooking = Category.objects.create(
        name = u"Vaření",
        slug = u"vareni-dortu",
    )
    case.category_cooking_cakes = Category.objects.create(
        name = u"Vaření dortů",
        slug = u"vareni-dortu",
        parent = case.category_cooking,
    )

    # nested unicode category with multiple childrens
    case.category_languages = Category.objects.create(
        name = u"Jazyky",
        slug = u"jazyky",
    )

    case.category_languages_chinese = Category.objects.create(
        name = u"汉语",
        slug = u"han-yu",
        parent = case.category_languages,
    )

    case.category_languages_chinese_confucius = Category.objects.create(
        name = u"孔夫子得哲学",
        slug = u"kong-fuzi-de-zhexue",
        parent = case.category_languages_chinese,
    )

    case.category_languages_japanese = Category.objects.create(
        name = u"日本語",
        slug = u"japanese",
        parent = case.category_languages,
    )

    case.category_languages_hindu = Category.objects.create(
        name = u"हिन्दी",
        slug = u"hindonese",
        parent = case.category_languages,
    )

    # flat category

    case.category_sex = Category.objects.create(
        name = u"Sex",
        slug = u"sex",
    )

    if commit:
        case.transaction.commit()