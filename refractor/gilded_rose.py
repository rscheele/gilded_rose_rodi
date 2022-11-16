# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            base_item = BaseItem(item.name, item.sell_in, item.quality)

            match item.name:
                case "Aged Brie":
                    child_item = AgedBrie(base_item.name, base_item.sell_in, base_item.quality)
                case "Sulfuras, Hand of Ragnaros":
                    child_item = Sulfuras(base_item.name, base_item.sell_in, base_item.quality)
                case "Backstage passes to a TAFKAL80ETC concert":
                    child_item = BackStagePass(base_item.name, base_item.sell_in, base_item.quality)
                case "Conjured Mana Cake":
                    child_item = Conjured(base_item.name, base_item.sell_in, base_item.quality)
                case _:
                    child_item = base_item

            child_item.daily_routine()

            item.quality = child_item.quality
            item.sell_in = child_item.sell_in


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class BaseItem(Item):
    def __init__(self, name, sell_in, quality, default_quality_increment=1, max_quality=50, min_quality=0,
                 legendary_quality=80):
        super().__init__(name, sell_in, quality)
        self.max_quality = max_quality
        self.min_quality = min_quality
        self.legendary_quality = legendary_quality
        self.default_quality_increment = default_quality_increment

    def daily_routine(self):
        self.daily_sell_in()
        self.daily_quality()

    def daily_quality(self):
        if self.quality > self.min_quality:
            if self.sell_in <= 0:
                self.quality -= self.default_quality_increment * 2
            else:
                self.quality -= self.default_quality_increment

    def daily_sell_in(self):
        self.sell_in -= 1


class AgedBrie(BaseItem):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def daily_quality(self):
        if self.quality < self.max_quality:
            self.quality += self.default_quality_increment


class Sulfuras(BaseItem):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def daily_quality(self):
        self.quality = self.legendary_quality

    def daily_sell_in(self):
        self.sell_in = self.sell_in


class BackStagePass(BaseItem):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def daily_quality(self):
        match self.sell_in:
            case i if i == 0:
                self.quality = 0
            case i if 1 <= i <= 5:
                self.quality += 3
            case i if 6 <= i <= 10:
                self.quality += 2
            case _:
                self.quality += 1

        if self.quality > self.max_quality:
            self.quality = self.max_quality


class Conjured(BaseItem):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def daily_quality(self):
        self.quality -= self.default_quality_increment * 2
