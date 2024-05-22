from decouple import config
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from helpers.send_email import create_and_send_email
from io import StringIO
import tkinter as tk
from tkinter import messagebox


class get_values_and_send_email:
    def __init__(self) -> None:
        super(get_values_and_send_email, self).__init__()
        driver = webdriver.Chrome()
        driver.maximize_window()

        self.login(driver)

        self.reset_data(driver)
        data_frame = pd.DataFrame(
            columns=[
                "WIID",
                "Description",
                "Type",
                "Status",
                "Date",
            ]
        )
        data_frame = self.get_data(driver, data_frame)
        type_counts, total_lines = self.show_message(data_frame)
        writer = pd.ExcelWriter(f"./teste_t2group.xlsx", engine="xlsxwriter")
        data_frame.to_excel(writer, index=False)
        writer.close()
        create_and_send_email("./teste_t2group.xlsx", type_counts, total_lines)

    def show_message(self, data_frame):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Total de linhas", f"{len(data_frame)} linhas!")
        messagebox.showinfo(
            "Valores",
            data_frame["Type"].value_counts().reset_index().to_string(index=False),
        )
        return data_frame["Type"].value_counts(), len(data_frame)

    def get_data(self, driver, data_frame):
        driver.get("https://acme-test.uipath.com/work-items")
        for page in range(self.get_total_pages(driver) + 1):
            page = page + 2
            df = self.get_data_frame(driver)
            df = df[self.column_list()]
            for _, data in df.iterrows():
                data_record = {
                    "WIID": data["WIID"],
                    "Description": data["Description"],
                    "Type": data["Type"],
                    "Status": data["Status"],
                    "Date": data["Date"],
                }
                data_frame.loc[len(data_frame)] = data_record
            if page >= self.get_total_pages(driver) + 1:
                break
            else:
                WebDriverWait(driver, timeout=20).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//a[text()='{page}']",
                        )
                    )
                ).click()

        return data_frame

    def get_total_pages(self, driver):
        pagination_list = WebDriverWait(driver, timeout=20).until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "page-numbers",
                )
            )
        )

        page_links = pagination_list.find_elements(By.TAG_NAME, "a")
        page_numbers = []
        for link in page_links:
            href = link.get_attribute("href")
            if "page=" in href:
                page_number = int(href.split("page=")[-1])
                page_numbers.append(page_number)
        return max(page_numbers)

    @staticmethod
    def column_list():
        return [
            "WIID",
            "Description",
            "Type",
            "Status",
            "Date",
        ]

    def get_data_frame(self, driver):
        data_frame = (
            WebDriverWait(driver, timeout=20)
            .until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div/div[2]/div[1]/table",
                    )
                )
            )
            .get_attribute("outerHTML")
        )
        return pd.read_html(StringIO(str(data_frame)))[0]

    def reset_data(self, driver):
        driver.get("https://acme-test.uipath.com/reset-test-data")
        WebDriverWait(driver, timeout=10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div/div[2]/div/div/button",
                )
            )
        ).click()
        WebDriverWait(driver, timeout=20).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

    def login(self, driver):
        driver.get("https://acme-test.uipath.com")
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div[2]/div/div/div/form/div[1]/div/input",
                )
            )
        ).send_keys(config("USER"))
        WebDriverWait(driver, timeout=10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div/div[2]/div/div/div/form/div[2]/div/input",
                )
            )
        ).send_keys(config("PWD"))
        WebDriverWait(driver, timeout=10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div/div[2]/div/div/div/form/button",
                )
            )
        ).click()
