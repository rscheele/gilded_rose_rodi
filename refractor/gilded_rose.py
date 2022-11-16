# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        """The item object called by the legacy system. Should not be changed.

        Args:
            name (str): The name of an item
            sell_in (int): The sell in value of an item
            quality (int): The quality value of an item
        """
        self.name: str = name
        self.sell_in: int = sell_in
        self.quality: int = quality

    def __repr__(self) -> str:
        """Returns string representation of the object.

        Returns:
            str: String containing the name, sell_in and quality values of the item.
        """
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class GildedRose(object):
    def __init__(self, items: list[Item]) -> None:
        """Gildedrose object used by the legacy system.

        Args:
            items (list[Item]): A list containing Item objects.
        """
        self.items: list[Item] = items

    def update_quality(self) -> None:
        """This method is used by the legacy system thus it should not be renamed.
        
        It updates the quality of items, where one call equals one day.
        """
        for item in self.items:

            base_item = BaseItem(item.name, item.sell_in, item.quality)

            match item.name:
                case "Aged Brie":
                    child_item = AgedBrie(base_item.name, base_item.sell_in, base_item.quality)
                case "Sulfuras, Hand of Ragnaros":
                    child_item = Sulfuras(base_item.name, base_item.sell_in, base_item.quality, 1, 80, 0)
                case "Backstage passes to a TAFKAL80ETC concert":
                    child_item = BackStagePass(base_item.name, base_item.sell_in, base_item.quality)
                case "Conjured Mana Cake":
                    child_item = Conjured(base_item.name, base_item.sell_in, base_item.quality)
                case _:
                    child_item = base_item

            child_item.daily_routine()

            item.quality = child_item.quality
            item.sell_in = child_item.sell_in


class BaseItem(Item):
    def __init__(self, name: str, sell_in: int, quality: int, default_quality_increment: int=1, max_quality: int=50, min_quality: int=0) -> None:
        """BaseItem class inheriting the original Item class, it contains extended functionality from the original function.

        Args:
            name (str): Name of the item
            sell_in (int): Sell in value of the item
            quality (int): Quality value of the item
            default_quality_increment (int, optional): Default quality increment value. Defaults to 1.
            max_quality (int, optional): Maximum quality value of an item. Defaults to 50.
            min_quality (int, optional): Minumum quality value of an item. Defaults to 0.
        """
        super().__init__(name, sell_in, quality)
        self.max_quality: int = max_quality
        self.min_quality: int = min_quality
        self.default_quality_increment: int = default_quality_increment

    def daily_routine(self) -> None:
        """Execute the daily routine by running the sell in and quality routines.
        """
        self.daily_sell_in()
        self.daily_quality()

    def daily_quality(self) -> None:
        """Execute the base daily quality routine.
        """
        if self.quality > self.min_quality:
            if self.sell_in <= 0:
                self.quality -= self.default_quality_increment * 2
            else:
                self.quality -= self.default_quality_increment
            if self.quality < self.min_quality:
                self.quality = self.min_quality

    def daily_sell_in(self) -> None:
        """Execute the base daily sell in routine.
        """
        self.sell_in -= 1


class AgedBrie(BaseItem):
    def __init__(self, name, sell_in, quality, default_quality_increment, max_quality, min_quality):
        super().__init__(name, sell_in, quality, default_quality_increment, max_quality, min_quality)

    def daily_quality(self):
        if self.quality < self.max_quality:
            self.quality += self.default_quality_increment


class Sulfuras(BaseItem):
    def __init__(self, name, sell_in, quality, default_quality_increment, max_quality, min_quality):
        super().__init__(name, sell_in, quality, default_quality_increment, max_quality, min_quality)

    def daily_quality(self):
        self.quality = self.max_quality

    def daily_sell_in(self):
        self.sell_in = self.sell_in


class BackStagePass(BaseItem):
    def __init__(self, name, sell_in, quality, default_quality_increment, max_quality, min_quality):
        super().__init__(name, sell_in, quality, default_quality_increment, max_quality, min_quality)

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
    def __init__(self, name, sell_in, quality, default_quality_increment, max_quality, min_quality):
        super().__init__(name, sell_in, quality, default_quality_increment, max_quality, min_quality)

    def daily_quality(self):
        if self.quality > self.min_quality:
            self.quality -= self.default_quality_increment * 2
            if self.quality < self.min_quality:
                self.quality = self.min_quality
