# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime


class TrainPipeline(object):

    def process_item(self, item, spider):
        print("Saving item", item["subject"])
        with open('data.csv', mode='a') as csv_file:
            fieldnames = ['subject', 'predicate', 'object', 'time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(item)
        return item
