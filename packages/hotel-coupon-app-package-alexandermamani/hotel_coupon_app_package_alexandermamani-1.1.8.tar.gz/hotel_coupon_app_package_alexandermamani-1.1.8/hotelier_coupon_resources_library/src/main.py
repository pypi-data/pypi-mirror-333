from hotel_coupon_app_package_alexandermamani.report_pdf import ReportPDF
from src.hotel_coupon_app_package_alexandermamani.report_pdf import ReportCustomPDF


def main1():
    coupon_gral_information = {}
    coupon_gral_information['1'] = {}
    coupon_gral_information['1']['title'] = "December offer"
    coupon_gral_information['1']['how_many_have_redeemed'] = "2"
    coupon_gral_information['1']['how_many_have_used'] = "1"
    coupon_gral_information['1']['quantity'] = "30"
    coupon_gral_information['1']['discount'] = "10"
    coupon_gral_information['2'] = {}
    coupon_gral_information['2']['title'] = "January offer"
    coupon_gral_information['2']['how_many_have_redeemed'] = "0"
    coupon_gral_information['2']['how_many_have_used'] = "0"
    coupon_gral_information['2']['quantity'] = "15"
    coupon_gral_information['2']['discount'] = "5"

    user_interactions = {}
    user_interactions["1"] = {}
    user_interactions["1"]['view'] = 0
    user_interactions["1"]['redeem'] = 0
    user_interactions["1"]['coupon_title'] = "Winter promotion"
    user_interactions["2"] = {}
    user_interactions["2"]['view'] = 10
    user_interactions["2"]['redeem'] = 10
    user_interactions["2"]['coupon_title'] = "Summer promotion"

    report = ReportPDF(user_interactions, coupon_gral_information, datetime.datetime.now().date(), "Dublin hotel",
                       "report.pdf")
    print(report.generate())

def main2():
    data = {}

    data['order_id'] = "order_id"
    data['name'] = "name"
    data['email'] = "email"
    data['shipping_address'] = "shipping_address"
    data['total'] = "total"

    data['report_title'] = "Report Name"
    data['report_description'] = "This is an example of a report description"
    data['report_table_data_header'] = {"column1": "Order id", "column2": "Product name", "column3": "Quantity", "column4": "Price"}
    data['report_table_data_body'] = [
                                        {"column1": "12j-jk12-12", "column2": "Car 1", "column3": "12", "column4": "13.45"},
                                        {"column1": "12j-jk12-33", "column2": "Car 1", "column3": "12", "column4": "13.45"}
                                      ]
    report = ReportCustomPDF(data, "report.pdf")
    print(report.generate())


import datetime
if __name__ == '__main__':

    main2()
