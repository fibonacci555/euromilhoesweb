
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup

numeros_full = []
id = 0

def readAll(ano):
    global numeros_full
    global id

    url = "https://www.euro-millions.com/results-history-" + str(ano)
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.text, "lxml")
        rows = soup.find_all('tr', class_='resultRow')
        for row in rows:
            edicao = [id]

            # Get the date
            date_td = row.find('td', class_='date noBefore')
            date_str = date_td.get_text(strip=True) if date_td else ''

            # Get the main numbers
            balls_li = row.find_all('li', class_='resultBall ball small')
            numbers = [li.get_text(strip=True).zfill(2) for li in balls_li]

            # Get the lucky stars
            lucky_stars_li = row.find_all('li', class_='resultBall lucky-star small')
            lucky_stars = [li.get_text(strip=True).zfill(2) for li in lucky_stars_li]

            # Get raffle code
            raffle_td = row.find('td', {'data-title': 'Millionaire Maker'})
            raffle_code = raffle_td.get_text(strip=True) if raffle_td else ''

            # Get jackpot amount
            jackpot_td = row.find('td', {'data-title': 'Jackpot'})
            jackpot_strong = jackpot_td.find('strong') if jackpot_td else None
            jackpot = jackpot_strong.get_text(strip=True) if jackpot_strong else ''

            # Append data to the list
            edicao.append(date_str)
            edicao.extend(numbers)
            edicao.extend(lucky_stars)
            edicao.append(raffle_code)
            edicao.append(jackpot)

            numeros_full.append(edicao)
            id += 1

        print(f"Scraped {id} draws for year {ano}")
    else:
        print(f"Failed to retrieve data for year {ano}")
        

def start(filename):
    sheettitle = 'Numeros'

    # Scrape data for years 2009 to 2022
    for i in range(2009, 2025):
        readAll(i)

    wb = Workbook()
    wb['Sheet'].title = sheettitle
    sh1 = wb.active

    # Define headers
    sh1['A1'].value = 'ID'
    sh1['B1'].value = 'Date'
    sh1['C1'].value = 'Numero1'
    sh1['D1'].value = 'Numero2'
    sh1['E1'].value = 'Numero3'
    sh1['F1'].value = 'Numero4'
    sh1['G1'].value = 'Numero5'
    sh1['H1'].value = 'Estrela1'
    sh1['I1'].value = 'Estrela2'
    sh1['J1'].value = 'RaffleCode'
    sh1['K1'].value = 'Jackpot'
    sh1['L1'].value = 'Numero Completo'

    # Write data to Excel
    for i in range(len(numeros_full)):
        row_num = i + 2  # Starting from row 2 since row 1 is the header

        draw = numeros_full[i]

        sh1[f'A{row_num}'].value = draw[0]  # ID
        sh1[f'B{row_num}'].value = draw[1]  # Date
        sh1[f'C{row_num}'].value = draw[2]  # Numero1
        sh1[f'D{row_num}'].value = draw[3]  # Numero2
        sh1[f'E{row_num}'].value = draw[4]  # Numero3
        sh1[f'F{row_num}'].value = draw[5]  # Numero4
        sh1[f'G{row_num}'].value = draw[6]  # Numero5
        sh1[f'H{row_num}'].value = draw[7]  # Estrela1
        sh1[f'I{row_num}'].value = draw[8]  # Estrela2
        sh1[f'J{row_num}'].value = draw[9]  # RaffleCode
        sh1[f'K{row_num}'].value = draw[10]  # Jackpot

        # Concatenate numbers and stars to create 'Numero Completo'
        numero_completo = ''.join(draw[2:9])  # From Numero1 to Estrela2
        sh1[f'L{row_num}'].value = numero_completo

    try:
        wb.save(filename)
        print(f"Data successfully saved to {filename}")
    except PermissionError:
        print('File might be opened, please close it before writing')

if __name__ == "__main__":
    start('results.xlsx')