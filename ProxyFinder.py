"""A GUI app that finds fresh proxies, filters and saves them to a .txt file."""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename

import requests
from bs4 import BeautifulSoup


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Proxies Finder v0.1")

        self.label = tk.Label(self, text="Select your options and click the Get Proxies button.", padx=5, pady=5)
        self.label.pack(side=tk.TOP, padx=5, pady=5)

        self.top_frame = ttk.Frame(self)
        self.top_frame.pack(side=tk.TOP)

        self.use_https = tk.BooleanVar()
        self.use_https.set(True)
        self.https_check = ttk.Checkbutton(self.top_frame, text="HTTPS?", variable=self.use_https, onvalue=True, offvalue=False)
        self.https_check.pack(side=tk.LEFT, padx=10, pady=5)

        proxy_levels = ["Anonymity Level", "elite proxy", "anonymous", "transparent"]

        self.selected_level = tk.StringVar()
        self.levels_dropdown = ttk.OptionMenu(self.top_frame, self.selected_level, *proxy_levels)
        self.levels_dropdown.configure(width=20)
        self.levels_dropdown.pack(side=tk.LEFT, padx=10, pady=5)

        self.do_button = ttk.Button(self.top_frame, text="Get Proxies", command=self.load_data)
        self.do_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.tree = ttk.Treeview(self, columns=["Anonymity", "HTTPS", "IP", "Port", "Country"])
        self.tree["show"] = "headings"
        
        self.tree.heading("#1", text="Anonymity")
        self.tree.heading("#2", text="HTTPS")
        self.tree.heading("#3", text="IP Address")
        self.tree.heading("#4", text="Port")
        self.tree.heading("#5", text="Country")

        self.tree.column("#1", stretch=tk.NO, width=150, anchor=tk.W)
        self.tree.column("#2", stretch=tk.NO, width=150, anchor=tk.W)
        self.tree.column("#3", stretch=tk.NO, anchor=tk.W)
        self.tree.column("#4", stretch=tk.NO, width=100, anchor=tk.W)
        self.tree.column("#5", stretch=tk.NO, width=200, anchor=tk.W)

        self.tree.pack(side=tk.TOP, expand=1, padx=5, pady=5, fill=tk.BOTH)

        self.save_button = ttk.Button(self, text="Save to File", width=20, command=self.save_file)
        self.save_button.pack(side=tk.TOP, padx=5, pady=10)

    def load_data(self):
        """Clears the TreeView and populates it again with fresh data."""

        if self.selected_level.get() != "Anonymity Level":

            for old_item in self.tree.get_children():
                self.tree.delete(old_item)

            for item in self.get_proxy_list():
                self.tree.insert("", "end", values=[item[0], item[1], item[2], item[3], item[4]])

    def get_proxy_list(self):
        """Gets a list of available free proxies and filters them."""

        url = "https://free-proxy-list.net/"

        with requests.get(url) as proxy_response:

            soup = BeautifulSoup(proxy_response.text, "html.parser")

            table = soup.find("table", class_="table table-striped table-bordered").find("tbody")
            proxy_list = []

            for row in table.find_all("tr"):
                proxy_data = row.find_all("td")
                proxy_anonymity = proxy_data[4].text
                proxy_https = proxy_data[6].text
                proxy_ip = proxy_data[0].text
                proxy_port = proxy_data[1].text
                proxy_country = proxy_data[3].text

                if self.use_https.get() == True and proxy_https == "yes" and proxy_anonymity == self.selected_level.get():
                    proxy_list.append([proxy_anonymity, proxy_https, proxy_ip, proxy_port, proxy_country])
                elif self.use_https.get() == False and proxy_https == "no" and proxy_anonymity == self.selected_level.get():
                    proxy_list.append([proxy_anonymity, proxy_https, proxy_ip, proxy_port, proxy_country])

            return proxy_list

    def save_file(self):
        """Saves the filtered results into a .txt file."""

        temp_file_name = asksaveasfilename(defaultextension=".txt")
        temp_file = open(temp_file_name, "w", encoding="utf-8", newline="")

        for row in self.tree.get_children():
            row_data = self.tree.item(row)["values"]
            temp_file.write("{}:{}\n".format(row_data[2], row_data[3]))

        temp_file.close()

if __name__ == "__main__":
    root = Root()
    root.minsize(800, 600)
    root.mainloop()
