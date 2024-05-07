import pdfplumber
import pandas as pd


# Function to extract tables from a PDF and save as CSV

#MOZAMBIQUE
# def extract_tables_from_Mozambique_pdf(pdf_file_path, output_csv_path):
#     extracted_tables = []

#     with pdfplumber.open(pdf_file_path) as pdf:
#         for i in range(14, 38, 2):  # Iterate through the pages by 2 for each full table
#             # Extract tables from the current page and the next page
#             page1 = pdf.pages[i ]
#             page2 = pdf.pages[i+1]
#             table_page_1 = page1.extract_table()
#             table_page_2 = page2.extract_table()

#             if table_page_1 and table_page_2:
#                 columns_1 = ['Food code', 'Food item', 'Energy(kj)', 'Energy(kcal)', 'Water(g)', 'Protein(g)','Fat total(g)', 'Carbohydrate(g)', 'Dietary fibre total(g)', 'Ash(g)', 'Alcohol(g)', 'Vitamin A RAE (Microgram (μg))', 'Retinol RAE (Microgram (μg))', ' Vitamin E(mg)', 'Thiamine (Vit B1(mg))', 'Riboflavin (Vit B2(mg))', 'Niacin(mg)', 'Pyridoxine (Vit B6(mg))', 'Folate(Microgram (μg))', 'Vitamin B12(Microgram (μg))']  # Column names for page 1
#                 columns_2 = ['Food code', 'Food item', 'Vitamin C(mg)', 'Sodium(mg)', 'Potassium(mg)', 'Calcium(mg)', 'Magnesium(mg)', 'Phosphorus(mg)', 'Iron(mg)', 'Zinc(mg)', 'Saturated fatty acids(g)', 'Monounsaturated fatty acids(g)', 'Polyunsaturated fatty acids(g)', 'C18:2 fatty acids (Linoleic acid)(g)', 'ɴ-carotene(Microgram (μg))', 'ɲ-carotene(Microgram (μg))', 'Cryptoxanthin(Microgram (μg))', 'Lycopene(Microgram (μg))', 'Lutein(Microgram (μg))']  # Column names for page 2

#                 # Create DataFrames for each page's table using respective column names
#                 df_page_1 = pd.DataFrame(table_page_1[0:], columns=columns_1[:len(table_page_1[0])])
#                 df_page_2 = pd.DataFrame(table_page_2[0:], columns=columns_2[:len(table_page_2[0])])
                                                                                
#                 # Add a new column 'Miscellaneous' with 0 values to the second table
#                 if len(columns_1) != len(columns_2):
#                     df_page_2['Miscellaneous'] = 0
#                 else:
#                     df_page_1['Miscellaneous'] = 0

#                 # Append the tables to the list
#                 extracted_tables.extend([df_page_1, df_page_2])

#        # Concatenate all extracted tables into one DataFrame
#     if extracted_tables:
#         final_table = pd.concat(extracted_tables, ignore_index=True)

#         # Save the combined table as a CSV file
#         final_table.to_csv(output_csv_path, index=False)
#     else:
#         print("No valid tables found for extraction.")
  


#ARMENIAN 
def extract_tables_from_Armenian_pdf(pdf_file_path, output_csv_path):
    extracted_tables = []

    with pdfplumber.open(pdf_file_path) as pdf:
        for i in range(17, 41, 3):  # Iterate through the pages by 2 for each full table
            # Extract tables from the current page and the next page
            page1 = pdf.pages[i]
            page2 = pdf.pages[i + 2]
            table_page_1 = page1.extract_table()
            table_page_2 = page2.extract_table()
           

            if table_page_1 and table_page_2:
                columns_1 = ['Food code', 'Food item-Armenian', 'food item-English', 'Source', 'Edible part', 'Energy(kcal)kj', 'Water(g)', 'white piles', 'Carbohydrate(g)', 'Dietary fibre total(g)','Food code', 'Food item-English', 'Fat total(g)', 'Saturated fatty acids(g)', 'Monounsaturated fatty acids(g)', 'Polyunsaturated fatty acids(g)', 'Trans fatty acid(g)', 'Cholesterol', 'Dry remainder', 'Calcium(mg)', 'Iron(mg)', 'Magnesium(mg)', 'Phosphorus(mg)', 'Potassium(mg)', 'Sodium(mg)', 'Zinc(mg)', 'Copper(mg)']
                columns_2 = ['Food code', 'Food item-English', 'Selenium (Microgram (μg))', 'Iodine (Microgram (μg))', 'Manganese(mg)', 'Vitamin A RAE (Microgram (μg))', 'Retinol RAE (Microgram (μg))', 'carotene(Microgram (μg))', 'Vitamin D (Microgram (μg))', ' Vitamin E(mg)', 'Thiamine (Vit B1(mg))', 'Riboflavin (Vit B2(mg))', 'Niacin(mg)', 'Pyridoxine (Vit B6(mg))', 'Folic acid(Microgram (μg))', 'Vitamin B12(Microgram (μg))', 'Vitamin C(mg)']
            
                # Create DataFrames for each page's table using respective column names
                df_page_1 = pd.DataFrame(table_page_1[1:], columns=columns_1[:len(table_page_1[0])])
                df_page_2 = pd.DataFrame(table_page_2[1:], columns=columns_2[:len(table_page_2[0])])
              
                                                                                
                # Add Miscellaneous columns based on column mismatches
                if len(columns_1) != len(columns_2):
                    for i in range(3):
                        column_name = f'Miscellaneous_{i+1}'
                        df_page_1[column_name] = 0
                else: 
                    for i in range(3):
                        column_name = f'Miscellaneous_{i+1}'
                        df_page_2[column_name] = 0
              
                # Append the tables to the list
                extracted_tables.extend([df_page_1, df_page_2])

       # Concatenate all extracted tables into one DataFrame
    if extracted_tables:
        final_table = pd.concat(extracted_tables, ignore_index=True)

        # Save the combined table as a CSV file
        final_table.to_csv(output_csv_path, index=False)
    else:
        print("No valid tables found for extraction.")
  

#Example usage
pdf_file = 'C:/Users/HP/Documents/Food composition/ArmenianFoodCompositionTable2010.hy.en.pdf'
output_csv = 'C:/Users/HP/Documents/Food composition/Food_Composition/armenian.csv'

extract_tables_from_Armenian_pdf(pdf_file, output_csv)

