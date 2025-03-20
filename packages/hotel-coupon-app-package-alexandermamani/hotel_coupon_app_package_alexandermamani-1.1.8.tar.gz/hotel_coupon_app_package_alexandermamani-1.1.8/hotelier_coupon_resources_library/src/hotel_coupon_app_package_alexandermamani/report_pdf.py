"""
report_pdf.py

A Python custom library for generating reports PDF for the app hotel coupon

Author: Alexander Mamani Yucra
Version: 1.0.0
"""

import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
import io

class ReportCustomPDF:
    def __init__(self, data, fileName=None):
        self.data = data
        self.fileName = fileName
        self.current_day = datetime.datetime.now().date()
        self.range_dates_text = f"Report generated at {self.current_day}"
        self.order_id = self.data['order_id']
        self.name = self.data['name']
        self.email = self.data['email']
        self.shipping_address = self.data['shipping_address']
        self.total = self.data['total']

        if self.fileName:
            self.report = SimpleDocTemplate(self.fileName, pagesize=letter)
        else:
            self.buffer = io.BytesIO()
            self.report = SimpleDocTemplate(self.buffer, pagesize=letter)

    def set_styles(self):
        """
        Set the styles for the PDF Tables
        """
        style = TableStyle([
            ('BACKGROUND', (0, 0), (4, 0), colors.orange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ])

        border_styles = TableStyle(
            [
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
                ('LINEABOVE', (0, 2), (-1, 2), 2, colors.orange),
                ('GRID', (0, 0), (-1, -1), 2, colors.black),
            ]
        )

        self.table_general_information.setStyle(style)
        self.table_general_information.setStyle(border_styles)


    def get_data(self):
        data_set = []
        table_header = self.data['report_table_data_header']
        data_set.append([table_header['column1'], table_header['column2'], table_header['column3'], table_header['column4']])
        for value in self.data['report_table_data_body']:
            data_set.append([value['column1'], value['column2'], value['column3'], value['column4']])
        return data_set

    def generate(self):
        general_information_dataset = self.get_data()
        self.table_general_information = Table(general_information_dataset)
        self.set_styles()
        styles = getSampleStyleSheet()
        two_breakline = Paragraph("<br/><br/>", styles['BodyText'])
        one_breakline = Paragraph("<br/>", styles['Title'])
        title = Paragraph(self.data["report_title"], styles['Title'])
        range_dates_text = Paragraph(self.range_dates_text, styles['Heading2'])
        general_information_text = Paragraph(self.data["report_description"], styles['Heading2'])

        order_id = Paragraph(f'Order: {self.order_id}', styles['Heading2'])
        name = Paragraph(f'Name: {self.name}', styles['Heading2'])
        email = Paragraph(f'Email: {self.email}', styles['Heading2'])
        shipping_address = Paragraph(f'Shipping Address: {self.shipping_address}', styles['Heading2'])
        ordered_items_text = Paragraph(f'Ordered Items', styles['Heading1'])

        total = Paragraph(f'Total: {self.total}', styles['Heading2'])

        elems = []
        elems.append(title)
        elems.append(two_breakline)
        elems.append(range_dates_text)
        elems.append(two_breakline)
        elems.append(order_id)
        # elems.append(two_breakline)
        elems.append(name)
        # elems.append(two_breakline)
        elems.append(email)
        # elems.append(two_breakline)
        elems.append(shipping_address)
        elems.append(two_breakline)
        elems.append(ordered_items_text)

        # elems.append(general_information_text)
        elems.append(one_breakline)
        elems.append(self.table_general_information)

        elems.append(one_breakline)
        elems.append(total)

        self.report.build(elems)
        if not self.fileName:
            self.buffer.seek(0)
            return self.buffer


class ReportPDF:
    """
    ReportPDF Class Allows to create a custom Report PDF for the hotel coupon app. Listing the user interaction with the coupons and the general information about a specific hotelier's coupons.
    Generating two tables with the data.

    :param coupon_interaction_data: A dictionary with the user interaction data for the coupons.
    :param coupon_gral_information_data: A dictionary with the general information about the coupons.
    :param from_date_report: The initial range of date which the report is generated.
    :param hotelier_name: The name of the hotelier.
    :param fileName: The name of the file to save the report. None whe you want to return a Buffer of the PDF
    """

    def __init__(self, coupon_interaction_data, coupon_gral_information_data, from_date_report, hotelier_name, fileName=None):
        self.coupon_interaction_data = coupon_interaction_data
        self.coupon_gral_information_data = coupon_gral_information_data
        self.from_date_report = from_date_report
        self.hotelier_name = hotelier_name
        self.current_day = datetime.datetime.now().date()
        self.fileName = fileName
        self.title_text = f"{self.hotelier_name} Coupon Report"
        self.range_dates_text = f"User coupon interaction from {self.from_date_report} to {self.current_day}"
        self.general_information_text=f"General information about your coupons"
        if self.fileName:
            self.report = SimpleDocTemplate(self.fileName, pagesize=letter)
        else:
            self.buffer = io.BytesIO()
            self.report = SimpleDocTemplate(self.buffer, pagesize=letter)

    def proccess_user_interaction_data(self):
        """
        Proccess the user interaction data and return a list of lists with the data to be displayed in the PDF Table
        """
        data_set = []
        data_set.append(['Coupon Title', 'View', 'Redeems'])
        for key, value in self.coupon_interaction_data.items():
            data_set.append([value['coupon_title'], value['view'], value['redeem']])
        return data_set

    def proccess_general_information_coupon_data(self):
        """
        Proccess the general information about the coupons and return a list of lists with the data to be displayed in the PDF Table
        """
        data_set = []
        data_set.append(['Coupon Title', 'Quantity', 'Discount (%)', 'Redeemeds', 'Used'])
        for key, value in self.coupon_gral_information_data.items():
            data_set.append([value['title'], value['quantity'], value['discount'], value['how_many_have_redeemed'], value['how_many_have_used']])
        return data_set

    def set_styles(self):
        """
        Set the styles for the PDF Tables
        """
        style = TableStyle([
            ('BACKGROUND', (0, 0), (4, 0), colors.orange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ])

        border_styles = TableStyle(
            [
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
                ('LINEABOVE', (0, 2), (-1, 2), 2, colors.orange),
                ('GRID', (0, 0), (-1, -1), 2, colors.black),
            ]
        )

        self.table_user_interaction.setStyle(style)
        self.table_general_information.setStyle(style)
        self.table_user_interaction.setStyle(border_styles)
        self.table_general_information.setStyle(border_styles)

    def generate(self):
        """
        Build the PDF Report with the user interaction data and the general information about the coupons
        """
        user_interaction_dataset = self.proccess_user_interaction_data()
        general_information_dataset = self.proccess_general_information_coupon_data()

        self.table_user_interaction = Table(user_interaction_dataset)
        self.table_general_information = Table(general_information_dataset)
        self.set_styles()
        styles = getSampleStyleSheet()
        two_breakline = Paragraph("<br/><br/>", styles['BodyText'])
        one_breakline = Paragraph("<br/>", styles['Title'])
        title = Paragraph(self.title_text, styles['Title'])
        range_dates_text = Paragraph(self.range_dates_text, styles['Heading2'])
        general_information_text = Paragraph(self.general_information_text, styles['Heading2'])

        elems = []
        elems.append(title)
        elems.append(two_breakline)
        if len(user_interaction_dataset) == 1:
            elems.append(Paragraph("Your coupons have not been viewed or redeemed", styles['Heading3']))
        else:
            elems.append(range_dates_text)
            elems.append(one_breakline)
            elems.append(self.table_user_interaction)

        elems.append(two_breakline)
        elems.append(general_information_text)
        elems.append(one_breakline)
        elems.append(self.table_general_information)

        self.report.build(elems)
        if not self.fileName:
            self.buffer.seek(0)
            return self.buffer