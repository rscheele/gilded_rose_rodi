# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            match item.name:
                case "Aged Brie":
                    item = AgedBrie(item)
                case "Sulfuras, Hand of Ragnaros":
                    item = Sulfuras(item)
                case "Backstage passes to a TAFKAL80ETC concert":
                    item = BackStagePass(item)
                case "Conjured Mana Cake":
                    item = Conjured(item)
                case _:
                    item = BaseItem(item)

            item.daily_sell_in()
            item.daily_quality()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class BaseItem(Item):
    def __init__(self, item):
        self.item = item

    def daily_quality(self):
        if self.item.quality > 0:
            if self.item.sell_in <= 0:
                self.item.quality -= 2
            else:
                self.item.quality -= 1

    def daily_sell_in(self):
        self.item.sell_in -= 1


class AgedBrie(BaseItem):
    def __init__(self, item):
        self.item = item

    def daily_quality(self):
        if self.item.quality < 50:
            self.item.quality += 1


class Sulfuras(BaseItem):
    def __init__(self, item):
        self.item = item

    def daily_quality(self):
        self.item.quality = 80

    def daily_sell_in(self):
        self.item.sell_in = self.item.sell_in


class BackStagePass(BaseItem):
    def __init__(self, item):
        self.item = item

    def daily_quality(self):
        match self.item.sell_in:
            case i if i == 0:
                self.item.quality = 0
            case i if 1 <= i <= 5:
                self.item.quality += 3
            case i if 6 <= i <= 10:
                self.item.quality += 2
            case _:
                self.item.quality += 1

        if self.item.quality > 50:
            self.item.quality = 50


class Conjured(BaseItem):
    def __init__(self, item):
        self.item = item

    def daily_quality(self):
        self.item.quality -= 2
