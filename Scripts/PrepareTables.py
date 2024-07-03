import os.path
import pdb

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import numpy as np

filepath = '..\\Processed\\Throughputs\\'
throughputs_path = filepath + "ForQA_20240626"
class PrepareTables:
    def __init__(self, master_csd_filepath, master_cd_filepath, formulas_filepath):
        self.master_csd_filepath = master_csd_filepath
        self.master_cd_filepath = master_cd_filepath
        self.formulas_filepath = formulas_filepath
        self.master_csd_data = pd.read_excel(self.master_csd_filepath, header=[0, 1, 2])
        self.master_cd_data = pd.read_excel(self.master_cd_filepath, header=[0, 1, 2])
        self.formulas_data = pd.read_excel(self.formulas_filepath, sheet_name='Outputs')

        self.clean_master_csd_data = self.clean_input_data(self.master_csd_data)
        self.clean_master_cd_data = self.clean_input_data(self.master_cd_data)
        self.master_with_formula = self.apply_formula(self.clean_master_csd_data, self.formulas_data)

    def prepare_table_4(self):
        print("Preparing Table 4...")
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 4]
        output_columns = filtered_formulas_df['Output'].tolist()

        # # List of columns for the table which should have been calculated based on the formula spreadsheet
        # output_columns_t4a = ['Total Households Owner, 2006', 'Total Households Renter, 2006',
        #                       'Total Households Owner, 2011', 'Total Households Renter, 2011',
        #                       'Total Households Owner, 2016', 'Total Households Renter, 2016',
        #                       'Total Households Owner, 2021', 'Total Households Renter, 2021']

        # Pull id fields and calculated fields as above
        required_data_t4a = self.master_with_formula[
            ['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns[:8]]

        # # List of columns for the table which should have been calculated based on the formula spreadsheet
        # output_columns_t4b = ['Percent of owners with a mortgage in ECHN, 2021',
        #                       'Number of units needed for owners with a mortgage, 2021',
        #                       'Renters in ECHN, 2021', 'Renters in ECHN, 2006',
        #                       'Renters in ECHN, 2011', 'Renters in ECHN, 2016',
        #                       'Renters % of total in ECHN, 2021',
        #                       'Renters % of total in ECHN, 2006',
        #                       'Renters % of total in ECHN, 2011',
        #                       'Renters % of total in ECHN, 2016']

        # Pull id fields and calculated fields as above
        required_data_t4b = self.master_with_formula[
            ['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns[8:]]

        # Final tables
        table_4a = self.clean_table_4a_data(required_data_t4a, [2006, 2011, 2016, 2021])
        table_4b = self.clean_table_4b_data(required_data_t4b, [2006, 2011, 2016, 2021])

        # export to Excel
        path_to_save = os.path.join(throughputs_path, "Section A")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        # pdb.set_trace()
        table_4a.to_excel(os.path.join(path_to_save, "Table4a.xlsx"))
        table_4b.to_excel(os.path.join(path_to_save, "Table4b.xlsx"))
        print("Table 4 Successfully created...")

        return table_4a, table_4b

    def prepare_table_5(self, table_4b):
        print("Preparing Table 5...")
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 5]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns = filtered_formulas_df['Output'].tolist()

        # Pull id fields and calculated fields as above
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]
        # _, table_4b = self.prepare_table_4()

        table_5 = self.clean_table_5_data(required_data, table_4b)

        # Export to excel for QA
        path_to_save = os.path.join(throughputs_path, "Section A")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_5.to_excel(os.path.join(path_to_save, "Table5.xlsx"))
        print("Table 5 Successfully created...")
        return table_5

    def prepare_table_6(self):
        print("Preparing Table 6...")
        # This chunk is always the same
        # Get the info for the relevant table
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 6]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns = filtered_formulas_df['Output'].tolist()
        # pdb.set_trace()
        # Pull id fields and calculated fields as above
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + [output_columns[0]]]

        # Set the x's to 0's - this should happen in the apply_formula shouldn't it?
        # required_data.loc[required_data['Local Population, 2021'] == 'x', 'Local Population, 2021'] = 0

        # FOR CD DATA - Use the formula script lookup file to index the data we want from the CD file since the columns are the same
        required_csd_columns = filtered_formulas_df['Numerator'].tolist()
        # csd_columns = [244, 326]  # Population 2021 and PEH

        cd_columns = [c + 3 for c in required_csd_columns]

        # GEOUID, Name
        id_columns = [0, 1]
        req_columns = id_columns + cd_columns

        required_data_cd = self.clean_master_cd_data.iloc[:, req_columns]
        required_data_cd.columns = ['GEOUID', 'Name', 'CD Population', 'Regional PEH']  # rename

        # The sum has to be handled differently for certain regions. Adjust population per methodology.
        required_data_cd['Regional Population'] = required_data_cd['CD Population']
        required_data_cd.loc[required_data_cd['GEOUID'].isin([5943, 5945]), 'Regional Population'] = \
        required_data_cd.loc[required_data_cd['GEOUID'].isin([5943, 5945]), 'CD Population'].sum()
        required_data_cd.loc[required_data_cd['GEOUID'].isin([5959, 5955]), 'Regional Population'] = \
        required_data_cd.loc[required_data_cd['GEOUID'].isin([5959, 5955]), 'CD Population'].sum()

        table_6 = self.clean_table_6_data(required_data, required_data_cd)

        path_to_save = os.path.join(throughputs_path, "Section B")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_6.to_excel(os.path.join(path_to_save, "Table6.xlsx"))
        print("Table 6 Successfully created...")

        return table_6

    def prepare_table_7(self):
        print("Preparing Table 7...")
        # Apply the formula to each row
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 7]
        output_columns = filtered_formulas_df['Output'].tolist()
        # pdb.set_trace()
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]

        # TODO - change this to keep it dynamic
        # filtered_df = required_data[required_data['GEOUID'] == geoid_filter]

        # Process columns for each combination of year and category
        df_owner_2006 = self.clean_table_7_data(required_data, 2006, 'Owner').reset_index()
        df_owner_2021 = self.clean_table_7_data(required_data, 2021, 'Owner').reset_index()
        df_renter_2006 = self.clean_table_7_data(required_data, 2006, 'Renter').reset_index()
        df_renter_2021 = self.clean_table_7_data(required_data, 2021, 'Renter').reset_index()
        # pdb.set_trace()

        df_2006 = df_owner_2006.merge(df_renter_2006)
        df_2021 = df_owner_2021.merge(df_renter_2021)
        # pdb.set_trace()

        path_to_save = os.path.join(throughputs_path, "Section C")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        df_2006.to_excel(os.path.join(path_to_save, "Table7_2006.xlsx"))
        df_2021.to_excel(os.path.join(path_to_save, "Table7_2021.xlsx"))
        # pdb.set_trace()
        print("Table 7 Successfully created...")

        return df_2006, df_2021

    def prepare_table_8(self):
        print("Preparing Table 8...")
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 8]
        output_columns = filtered_formulas_df['Output'].tolist()
        # pdb.set_trace()
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]
        # TODO - change this to keep it dynamic
        # filtered_df = required_data[required_data['GEOUID'] == geoid_filter]
        # pdb.set_trace()

        df_2006 = self.clean_table_8_data(required_data, 2006).reset_index()
        df_2021 = self.clean_table_8_data(required_data, 2021).reset_index()
        # pdb.set_trace()

        table_8 = df_2006.merge(df_2021, on=[('GEOUID', ''), ('Municipality', ''),
                                             (' ', 'Age Categories – Household Maintainers'),
                                                      (' ', 'Age Categories – Population')])
        # pdb.set_trace()
        table_8 = table_8[[('GEOUID', ''), ('Municipality', ''), (' ', 'Age Categories – Household Maintainers'),
                           (' ', 'Age Categories – Population'), ('2006', 'All Categories'),
                           ('2006', 'Summed Categories'), ('2021', 'All Categories'), ('2021', 'Summed Categories')]]
        # table_8.columns = table_8.columns[:2] + [(' ', 'Age Categories – Household Maintainers'),
        #                                          (' ', 'Age Categories – Population')] + table_8.columns[4:]
        path_to_save = os.path.join(throughputs_path, "Section C")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_8.to_excel(os.path.join(path_to_save, "Table8.xlsx"))
        # pdb.set_trace()
        print("Table 8 Successfully created...")
        return table_8

    def prepare_table_9_10(self, table7_2006, table8):
        print("Preparing Table 9 and 10...")
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 9]
        output_columns = filtered_formulas_df['Output'].tolist()
        # pdb.set_trace()
        required_data = self.master_with_formula[
            ['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]
        # TODO - change this to keep it dynamic
        # filtered_df = required_data[required_data['GEOUID'] == geoid_filter]

        updated_table_7_2006 = table7_2006.replace('Under 25 years', '15 to 24 years')

        headship_rate_2006_owner = self.clean_table_9_data(required_data, 2006, 'Owner')
        headship_rate_2006_renter = self.clean_table_9_data(required_data, 2006, 'Renter')
        headship_rate_2006 = headship_rate_2006_owner.join(headship_rate_2006_renter).reset_index()
        # pdb.set_trace()

        table_9 = updated_table_7_2006.merge(table8.reset_index()[[('GEOUID', ''), ('Municipality', ''),
            (' ', 'Age Categories – Household Maintainers'), ('2006', 'Summed Categories')]],
                                        left_on=[(' ', 'Age – Primary Household Maintainer 2006 Categories'), ('Municipality', ''), ('GEOUID', '')],
                                    right_on=[(' ', 'Age Categories – Household Maintainers'), ('Municipality', ''), ('GEOUID', '')]).merge(
            headship_rate_2006, left_on=[(' ', 'Age Categories – Household Maintainers'), ('Municipality', ''), ('GEOUID', '')],
            right_on=[('Age Categories – Household Maintainers', ''), ('Municipality', ''), ('GEOUID', '')]
        )
        # pdb.set_trace()
        # table_9 = table_9.dropna(subset=[('2006', 'Summed Categories')])
        table_9.columns = pd.MultiIndex.from_tuples([('2006 Population', 'Total') if col == ('2006', 'Summed Categories') else col for col in table_9.columns])

        # pdb.set_trace()
        table_9 = table_9[[('GEOUID', ''), ('Municipality', ''), ('Age Categories – Household Maintainers', ''),
                           ('2006 Households', 'Owner'), ('2006 Households', 'Renter'),
                           ('2006 Population', 'Total'),
                           ('2006 Headship Rate', 'Owner'), ('2006 Headship Rate', 'Renter')]]
        table_9.drop_duplicates(keep='first', inplace=True)

        table_10 = table_9[[('GEOUID', ''), ('Municipality', ''), ('Age Categories – Household Maintainers', ''),
                            ('2006 Headship Rate', 'Owner'), ('2006 Headship Rate', 'Renter')]].merge(
            table8.reset_index()[[('GEOUID', ''), ('Municipality', ''), (' ', 'Age Categories – Household Maintainers'),
                                  ('2021', 'Summed Categories')]], left_on=[('GEOUID', ''), ('Municipality', ''), ('Age Categories – Household Maintainers', '')],
        right_on=[('GEOUID', ''), ('Municipality', ''), (' ', 'Age Categories – Household Maintainers')])
        table_10[('2021', 'Summed Categories')] = table_10[
            ('2021', 'Summed Categories')].astype(str).str.replace('xx', '0').str.replace('0x', '0').fillna(0).astype(float)
        table_10[('2006 Headship Rate Float', 'Owner')] = table_10[('2006 Headship Rate', 'Owner')].fillna('0%').str.rstrip('%').astype(float) / 100.0
        table_10[('2006 Headship Rate Float', 'Renter')] = table_10[('2006 Headship Rate', 'Renter')].fillna('0%').str.rstrip('%').astype(float) / 100.0
        # pdb.set_trace()
        table_10[('2021 Potential Households', 'Owner')] = table_10[('2006 Headship Rate Float', 'Owner')] * table_10[
            ('2021', 'Summed Categories')]
        table_10[('2021 Potential Households', 'Renter')] = table_10[('2006 Headship Rate Float', 'Renter')] * table_10[
            ('2021', 'Summed Categories')]
        # table_10 = table_10.dropna(subset=[('2021', 'Summed Categories')])
        table_10.columns = pd.MultiIndex.from_tuples(
            [('2021 Population', 'Total') if col == ('2021', 'Summed Categories') else col for col in table_10.columns])
        table_10.drop([('2006 Headship Rate Float', 'Owner'), ('2006 Headship Rate Float', 'Renter'),
                       (' ', 'Age Categories – Household Maintainers')], axis=1, inplace=True)
        table_10.drop_duplicates(keep='first', inplace=True)
        # pdb.set_trace()
        path_to_save = os.path.join(throughputs_path, "Section C")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_9.to_excel(os.path.join(path_to_save, "Table9.xlsx"))
        table_10.to_excel(os.path.join(path_to_save, "Table10.xlsx"))
        # pdb.set_trace()
        print("Table 9 and 10 Successfully created...")

        return table_9, table_10

    def prepare_table_11(self, table_7_2021, table_10):
        print("Preparing Table 11...")
        updated_table_7_2021 = table_7_2021.groupby([('GEOUID', ''), ('Municipality', '')]).apply(self.clean_table_11_data).reset_index(drop=True)

        # To check if 2 rows are removed (75 to 84 years, 85 years and over) and one row is added (75 years or more)
        assert len(updated_table_7_2021) == len(table_7_2021) - table_7_2021[('Municipality', '')].nunique(), "Age merging failed"

        required_table_10 = table_10[[('GEOUID', ''), ('Municipality', ''), ('Age Categories – Household Maintainers', ''),
                                     ('2021 Potential Households', 'Owner'), ('2021 Potential Households', 'Renter')]]

        table_11 = required_table_10.merge(updated_table_7_2021, on=[('GEOUID', ''), ('Municipality', ''), ('Age Categories – Household Maintainers', '')])

        # table_11.drop([(' ', 'Age Categories – Household Maintainers')], axis=1, inplace=True)
        # pdb.set_trace()
        assert len(table_11) == len(required_table_10), 'Table 11 and Table 10 merge failed'

        table_11[('2021 Suppressed Households', 'Owner')] = table_11[('2021 Potential Households', 'Owner')] - \
                                                            table_11[('2021 Households', 'Owner')]
        table_11[('2021 Suppressed Households', 'Renter')] = table_11[('2021 Potential Households', 'Renter')] - \
                                                            table_11[('2021 Households', 'Renter')]
        table_11[('2021 Suppressed Households', 'Total')] = table_11.apply(
            lambda row: row[('2021 Suppressed Households', 'Owner')] + row[('2021 Suppressed Households', 'Renter')] if
            row[('2021 Suppressed Households', 'Owner')] + row[('2021 Suppressed Households', 'Renter')] > 0 else 0,
            axis=1
        )

        # Calculate the sum of the 'Total' column
        grouped = table_11.groupby([('GEOUID', ''), ('Municipality', '')])

        # Initialize an empty list to hold the sum rows
        sum_rows = []
        # pdb.set_trace()
        # Loop through each group to calculate the sum and create the sum row
        for group_id, group in grouped:
            total_sum = group[('2021 Suppressed Households', 'Total')].sum()

            # Create a new sum row with the calculated sum and the municipality
            sum_row = pd.DataFrame([{
                ('GEOUID', ''): group_id[0],
                ('Municipality', ''): group_id[1],
                ('Age Categories – Household Maintainers', ''): 'Total New Units – 20 Years',
                ('2021 Suppressed Households', 'Total'): total_sum
            }])

            # Append the sum row to the list
            sum_rows.append(sum_row)

        # Concatenate the sum rows with the original DataFrame
        sum_rows_df = pd.concat(sum_rows, ignore_index=True)
        table_11 = pd.concat([table_11, sum_rows_df], ignore_index=True)
        # pdb.set_trace()


        path_to_save = os.path.join(throughputs_path, "Section C")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        # pdb.set_trace()
        table_11.to_excel(os.path.join(path_to_save, "Table11.xlsx"))
        print("Table 11 Successfully created...")
        return table_11

    def prepare_table_12_13(self):
        print("Preparing Table 12 and 13...")
        # This chunk is always the same
        # Get the info for the relevant table
        filtered_formulas_df_12 = self.formulas_data[self.formulas_data['Table'] == 12]
        filtered_formulas_df_13 = self.formulas_data[self.formulas_data['Table'] == 13]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns_12 = filtered_formulas_df_12['Output'].tolist()
        output_columns_13 = filtered_formulas_df_13['Output'].tolist()

        # Pull id fields and calculated fields as above
        required_data_12 = self.master_with_formula[
            ['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns_12]
        required_data_13 = self.master_with_formula[
            ['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns_13]

        # FOR CD DATA - Use the formula script lookup file to index the data we want from the CD file since the columns are the same
        # csd_columns = [327, 329]  # Households 2021 and Households 2041
        required_csd_columns = filtered_formulas_df_13['Numerator'].tolist()
        cd_columns = [c + 3 for c in required_csd_columns]

        # GEOUID, Name
        id_columns = [0, 1]
        req_columns = id_columns + cd_columns

        required_data_cd = self.clean_master_cd_data.iloc[:, req_columns]
        required_data_cd.columns = ['GEOUID', 'Name', '2021', '2041']  # rename
        required_data_cd['Regional District Projections'] = 'Households'
        required_data_cd['Regional Growth Rate'] = ((required_data_cd['2041'] / required_data_cd['2021']) - 1) * 100

        table_12 = self.clean_table_12_data(required_data_12, required_data_cd)
        table_13 = self.clean_table_13_data(required_data_13, required_data_cd)
        # pdb.set_trace()
        table_13.columns = pd.MultiIndex.from_tuples(
            [("GEOUID", ""), ("Municipality", ""), ("Growth Scenarios", ""),
             ("Regional Growth Rate", ""), ("Households", "2021"), ("Households", "2041"), ("New Units", "")])

        path_to_save = os.path.join(throughputs_path, "Section D")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_12.to_excel(os.path.join(path_to_save, "Table12.xlsx"))
        table_13.to_excel(os.path.join(path_to_save, "Table13.xlsx"))

        print("Table 12 and 13 Successfully created...")
        return table_12, table_13

    def prepare_table_14(self):
        # This chunk is always the same
        # Get the info for the relevant table
        print('Preparing Table 14...')
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 14]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns = filtered_formulas_df['Output'].tolist()

        # Pull id fields and calculated fields as above
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]

        table_14 = self.clean_table_14_data(required_data)

        path_to_save = os.path.join(throughputs_path, "Section E")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_14.to_excel(os.path.join(path_to_save, "Table14.xlsx"))
        print("Table 14 Successfully created...")

        return table_14

    def prepare_table_15(self, table_5, table_6, table_11, table_14):
        print('Preparing Table 15...')
        # This chunk is always the same
        # Get the info for the relevant table
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 15]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns = filtered_formulas_df['Output'].tolist()

        # Pull id fields and calculated fields as above
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]

        a_table5_units = table_5.loc[table_5['Total Households'] == 'Total New Units - 20 years'][
            ['GEOUID', 'Municipality', 'Households in ECHN']]
        a_table5_units.columns = ['GEOUID', 'Municipality', 'Result']
        a_table5_units['Component'] = 'A. Extreme Core Housing Need'
        a_table5_units['order'] = 0

        b_table6_units = table_6.loc[table_6[(' ', 'Regional Population')] == 'Total New Units - 20 years'][
            [('GEOUID', ''), ('Municipality', ''), (' ', 'Proportional Local PEH')]]
        b_table6_units.columns = ['GEOUID', 'Municipality', 'Result']
        b_table6_units['Component'] = 'B. Persons Experiencing Homelessness'
        b_table6_units['order'] = 1

        # pdb.set_trace()
        c_table11_units = table_11.loc[table_11['Age Categories – Household Maintainers'] == 'Total New Units – 20 Years'][
            [('GEOUID', ''), ('Municipality', ''), ('2021 Suppressed Households', 'Total')]]
        c_table11_units.columns = ['GEOUID', 'Municipality', 'Result']
        c_table11_units['Component'] = 'C. Suppressed Household Formation'
        c_table11_units['order'] = 2

        e_table14_units = table_14.loc[table_14[''] == 'Total New Units - 20 Years'][
            ['GEOUID', 'Municipality', 'Estimated Number of Units']]
        e_table14_units.columns = ['GEOUID', 'Municipality', 'Result']
        e_table14_units['Component'] = 'E. Rental Vacancy Rate Adjustment'
        e_table14_units['order'] = 3

        all_units = a_table5_units.append(b_table6_units).append(c_table11_units).append(e_table14_units)
        # all_units.replace('X', np.nan, inplace=True)
        #
        # # Convert all columns to numeric
        # all_units['Result'] = all_units['Result'].apply(pd.to_numeric, errors='coerce')
        total = all_units.groupby(['GEOUID', 'Municipality'])[['Result']].sum()
        total['Component'] = 'Total'
        total['order'] = 4

        demand = required_data.copy()
        demand['Component'] = 'Demand Factor'
        demand.rename(columns={'Demand factor': 'Result'}, inplace=True)
        demand['order'] = 5

        # pdb.set_trace()
        final = demand.copy()
        final.set_index(['GEOUID', 'Municipality'], inplace=True)
        final = final.join(total, lsuffix='_demand', rsuffix="_total")
        final['Component'] = 'Total New Units - 20 years'
        final.rename(columns={
            'Result_demand': 'Demand factor',
            'Result_total': 'Total'}, inplace=True)
        final['Result'] = final['Demand factor'] * final['Total']
        final['order'] = 6

        total.reset_index(inplace=True)
        final.reset_index(inplace=True)

        cols = ['GEOUID', 'Municipality', 'Component', 'Result', 'order']

        result_df = all_units[cols].append(total[cols]).append(demand[cols]).append(final[cols])

        table_15 = result_df.sort_values(by=['Municipality', 'order'])
        table_15.drop(columns=['order'], inplace=True)

        path_to_save = os.path.join(throughputs_path, "Section F")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_15.to_excel(os.path.join(path_to_save, "Table15.xlsx"))
        print("Table 15 Successfully created...")
        return table_15

    def prepare_table_16(self, table_5, table_6, table_11, table_13, table_14, table_15):
        print("Preparing Table 16...")
        # This chunk is always the same
        # Get the info for the relevant table
        filtered_formulas_df = self.formulas_data[self.formulas_data['Table'] == 16.5]

        # List of columns to calculate which should have been calculated based on the formula spreadsheet
        output_columns = filtered_formulas_df['Output'].tolist()

        # Pull id fields and calculated fields as above
        required_data = self.master_with_formula[['GEOUID', 'Municipality', 'Regional District', 'CD_ID'] + output_columns]

        # FOR CD DATA - Use the formula script lookup file to index the data we want from the CD file since the columns are the same
        # csd_columns = [327, 328]  # Households 2021 and Households 2026
        required_csd_columns = filtered_formulas_df['Numerator'].tolist()
        cd_columns = [c + 3 for c in required_csd_columns]

        # GEOUID, Name
        id_columns = [0, 1]
        req_columns = id_columns + cd_columns

        required_data_cd = self.clean_master_cd_data.iloc[:, req_columns]
        required_data_cd.columns = ['GEOUID', 'Name', '2021', '2026']  # rename
        required_data_cd['Regional District Projections'] = 'Households'
        required_data_cd['Regional Growth Rate'] = ((required_data_cd['2026'] / required_data_cd['2021']) - 1) * 100

        table_16_5yr = self.clean_table_16_5yr_data(required_data, required_data_cd)
        table_16_5yr_units = table_16_5yr.loc[table_16_5yr['Growth Scenarios'] == 'Total New Units - 5 years'][
            ['GEOUID', 'Municipality', 'New Units']]
        table_16_5yr_units.set_index(['GEOUID', 'Municipality'], inplace=True)

        a_table5_units = table_5.loc[table_5['Total Households'] == 'Total New Units - 20 years'][
            ['GEOUID', 'Municipality', 'Households in ECHN']]
        a_table5_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        # a_table5_units.replace('X', np.nan, inplace=True)
        #
        # # Convert all columns to numeric
        # a_table5_units['20 Year Need'] = a_table5_units['20 Year Need'].apply(pd.to_numeric, errors='coerce')
        a_table5_units['Component'] = 'A. Extreme Core Housing Need'
        a_table5_units['5 Year Need'] = a_table5_units['20 Year Need'] / 4
        a_table5_units['order'] = 0
        # pdb.set_trace()

        b_table6_units = table_6.loc[table_6[(' ', 'Regional Population')] == 'Total New Units - 20 years'][
            [('GEOUID', ''), ('Municipality', ''), (' ', 'Proportional Local PEH')]]
        b_table6_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        b_table6_units['Component'] = 'B. Persons Experiencing Homelessness'
        b_table6_units['5 Year Need'] = b_table6_units['20 Year Need'] / 2
        b_table6_units['order'] = 1

        c_table11_units = \
        table_11.loc[table_11['Age Categories – Household Maintainers'] == 'Total New Units – 20 Years'][
            [('GEOUID', ''), ('Municipality', ''), ('2021 Suppressed Households', 'Total')]]
        c_table11_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        c_table11_units['Component'] = 'C. Suppressed Household Formation'
        c_table11_units['5 Year Need'] = c_table11_units['20 Year Need'] / 4
        c_table11_units['order'] = 2

        # pdb.set_trace()
        d_table13_units = table_13.loc[table_13[('Growth Scenarios', '')] == 'Total New Units - 20 years'][
            [('GEOUID', ''), ('Municipality', ''), ('New Units', '')]]
        d_table13_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        d_table13_units['Component'] = 'D. Anticipated Growth'

        # 5 year need calculated in function above
        d_table13_units.set_index(['GEOUID', 'Municipality'], inplace=True)
        d_table13_units = d_table13_units.join(table_16_5yr_units)
        d_table13_units.reset_index(inplace=True)
        d_table13_units.rename(columns={'New Units': '5 Year Need'}, inplace=True)
        d_table13_units['order'] = 3

        e_table14_units = table_14.loc[table_14[''] == 'Total New Units - 20 Years'][
            ['GEOUID', 'Municipality', 'Estimated Number of Units']]
        e_table14_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        e_table14_units['Component'] = 'E. Rental Vacancy Rate Adjustment'
        e_table14_units['5 Year Need'] = e_table14_units['20 Year Need'] / 4
        e_table14_units['order'] = 4

        f_table15_units = table_15.loc[table_15['Component'] == 'Total New Units - 20 years'][
            ['GEOUID', 'Municipality', 'Result']]
        f_table15_units.columns = ['GEOUID', 'Municipality', '20 Year Need']
        f_table15_units['Component'] = 'F. Additional Local Demand'
        f_table15_units['5 Year Need'] = f_table15_units['20 Year Need'] / 4
        f_table15_units['order'] = 5

        cols = ['GEOUID', 'Municipality', 'Component', '5 Year Need', '20 Year Need', 'order']

        result_df = a_table5_units[cols].append(b_table6_units[cols]).append(c_table11_units[cols]).append(
            d_table13_units[cols]).append(e_table14_units[cols]).append(f_table15_units[cols])

        twenty = result_df.groupby(['GEOUID', 'Municipality'])[['20 Year Need']].sum()
        five = result_df.groupby(['GEOUID', 'Municipality'])[['5 Year Need']].sum()
        five['Component'] = 'Total New Units – 5 years'
        five['order'] = 6
        five.reset_index(inplace=True)
        twenty['Component'] = 'Total New Units – 20 years'
        twenty['order'] = 7
        twenty.reset_index(inplace=True)

        result_df = result_df.append(five).append(twenty)
        table_16 = result_df.sort_values(by=['Municipality', 'order']).dropna(subset=['GEOUID']).drop(columns=['order'])

        path_to_save = os.path.join(throughputs_path, "Section G")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        table_16.to_excel(os.path.join(path_to_save, "Table16.xlsx"))
        print("Table 16 successfully created...")

        return table_16




    @staticmethod
    def clean_table_4a_data(filtered_df, years):

        # Run through headings and concatenate the table
        for year in years:
            # Filter to the year
            columns = [col for col in filtered_df.columns if str(year) in col]
            df = filtered_df[columns + ['GEOUID', 'Municipality']]

            # Format the columns for reorg
            df.columns = pd.MultiIndex.from_tuples(
                [("Owner", year), ("Renter", year), ("", "GEOUID"), ("", "Municipality")])
            df.set_index(("", "GEOUID"), inplace=True)
            df.set_index(("", "Municipality"), append=True, inplace=True)

            # Transpose/stack the table to reorg
            df = df.stack(level=0).reset_index()

            # Rename columns to match table headings
            df.columns = ["GEOUID", "Municipality", "Total Households", year]
            df.set_index(["GEOUID", "Municipality", "Total Households"], inplace=True)

            if year == 2006:
                result_df = df.copy()
            else:
                result_df = result_df.join(df)

        result_df.reset_index(inplace=True)
        result_df = result_df[~result_df['Municipality'].isna()]

        return result_df

    @staticmethod
    def clean_table_4b_data(filtered_df, years):

        # Renters
        for year in years:
            # Filter to the year
            columns = [col for col in filtered_df.columns if str(year) in col and "Renters" in col]
            df = filtered_df[columns + ['GEOUID', 'Municipality']]

            # Format the columns for reorg
            df.columns = pd.MultiIndex.from_tuples(
                [(year, "#"), (year, "% of total"), ("", "GEOUID"), ("", "Municipality")])
            df.set_index(("", "GEOUID"), inplace=True)
            df.set_index(("", "Municipality"), append=True, inplace=True)

            # Join years together
            if year == 2006:
                renters = df.copy()
            else:
                renters = renters.join(df)

        # Calculate the Average ECHN Rate column
        avg_cols = [col for col in renters.columns if col[1] == '% of total']

        # They come in formatted with a % sign so they're strings. Remove it and calculate average.
        for c in avg_cols:
            renters[c] = renters[c].str.replace('%', '').astype(float)

        renters[('', 'Average ECHN Rate')] = renters[avg_cols].mean(axis=1)

        # Add the row id
        renters[('', 'Extreme Core Housing Need')] = 'Renters'

        # Owners
        if year == 2021:
            columns = [col for col in filtered_df.columns if str(year) in col and "owners" in col]
            owners = filtered_df[columns + ['GEOUID', 'Municipality']]
            owners.columns = pd.MultiIndex.from_tuples(
                [(year, "% of total"), (year, "#"), ("", "GEOUID"), ("", "Municipality")])
            owners.set_index(("", "GEOUID"), inplace=True)
            owners.set_index(("", "Municipality"), append=True, inplace=True)

            owners[('', 'Extreme Core Housing Need')] = 'Owners with a mortgage'
            owners[(year, "% of total")] = owners[(year, "% of total")].str.replace('%', '').astype(float)
            owners[('', 'Average ECHN Rate')] = owners[(year, "% of total")]

            result_df = pd.concat([owners, renters])

            # Reorder columns to match the table format
            column_order = [('', 'Extreme Core Housing Need'), (2006, '#'), (2006, '% of total'), (2011, '#'),
                            (2011, '% of total')
                , (2016, '#'), (2016, '% of total'), (2021, '#'), (2021, '% of total'), ('', 'Average ECHN Rate')]
            result_df = result_df[column_order]


        result_df = result_df.rename_axis(["GEOUID", "Municipality"])
        result_df = result_df.sort_values(by=['GEOUID', 'Municipality', ('', 'Extreme Core Housing Need')])

        result_df.reset_index(inplace=True)
        result_df = result_df[~result_df['Municipality'].isna()]

        return result_df

    @staticmethod
    def clean_table_5_data(filtered_df, table_4b):
        columns = [col for col in filtered_df.columns if str(2021) in col]
        df = filtered_df[columns + ['GEOUID', 'Municipality']]

        df.columns = pd.MultiIndex.from_tuples(
            [("Owners", "2021 Households"), ("Owners with a mortgage", "Households in ECHN"),
             ("Renters", "2021 Households"), ("", "GEOUID"), ("", "Municipality")])
        df.set_index(("", "GEOUID"), inplace=True)
        df.set_index(("", "Municipality"), append=True, inplace=True)

        unstacked_df = df.stack(level=0).reset_index()
        unstacked_df.columns = ['GEOUID', 'Municipality', 'Total Households', '2021 Households', 'Households in ECHN']
        unstacked_df['2021 Households'] = unstacked_df['2021 Households'].replace('x', np.nan).astype(float)

        # Join average ECHN rate from table 4b

        tojoin = table_4b[
            [('GEOUID', ''), ('Municipality', ''), ('', 'Extreme Core Housing Need'), ('', 'Average ECHN Rate')]]
        tojoin.columns = ['GEOUID', 'Municipality', 'Total Households', 'Average ECHN Rate']
        newdf = unstacked_df.merge(tojoin[['Average ECHN Rate', 'GEOUID', 'Municipality', 'Total Households']],
                                   left_on=['GEOUID', 'Municipality', 'Total Households'],
                                   right_on=['GEOUID', 'Municipality', 'Total Households'], how='outer')
        # pdb.set_trace()
        # calculate the units needed for renters
        newdf.loc[newdf['Total Households'] == 'Renters', 'Households in ECHN'] = newdf['2021 Households'] * (
                    newdf['Average ECHN Rate'].astype(float) / 100)
        # newdf.loc[newdf['2021 Households'].isna(), 'Households in ECHN'] = np.nan

        total_new_units = newdf.groupby(['GEOUID', 'Municipality'])[['Households in ECHN']].sum()
        total_new_units['Total Households'] = 'Total New Units - 20 years'
        total_new_units.reset_index(inplace=True)

        result_df = newdf.append(total_new_units).set_index(["GEOUID", "Municipality"])

        column_order = ['Total Households', '2021 Households', 'Average ECHN Rate', 'Households in ECHN']

        result_df = result_df[column_order]
        result_df.replace('X', np.nan, inplace=True)
        #
        # # Convert all columns to numeric
        result_df['Households in ECHN'] = result_df['Households in ECHN'].apply(pd.to_numeric, errors='coerce')
        result_df = result_df.sort_values(by=['Municipality', 'Total Households'])

        result_df.reset_index(inplace=True)

        return result_df

    @staticmethod
    def clean_table_6_data(filtered_df, filtered_df_cd):
        alldata = filtered_df.merge(filtered_df_cd, left_on='CD_ID', right_on='GEOUID', suffixes=('_CSD', '_CD'),
                                    how='outer')
        result_df = alldata[['GEOUID_CSD', 'GEOUID_CD', 'Municipality', 'Local Population, 2021', 'Regional Population',
                             'Regional PEH']]
        result_df = result_df.dropna(subset=['GEOUID_CSD', 'GEOUID_CD'], how='all')
        result_df.loc[~result_df['Local Population, 2021'].isna(), '% of region'] = result_df[
                                                                                        'Local Population, 2021'].astype(
            float) / result_df['Regional Population'].astype(int)
        result_df['Proportional Local PEH'] = result_df['% of region'] * result_df['Regional PEH']

        column_order = ['GEOUID_CSD', 'Municipality', 'Regional Population', 'Local Population, 2021', '% of region',
                        'Regional PEH', 'Proportional Local PEH']
        result_df = result_df[column_order]
        # result_df.columns = ['GEOUID', 'Municipality', 'Regional Population', 'Local Population, #', '% of region',
        #                      'Regional PEH', 'Proportional Local PEH']
        result_df.columns = pd.MultiIndex.from_tuples(
            [('GEOUID', ''), ('Municipality', ''), (' ', 'Regional Population'),
             ('Local Population', '#'), ('Local Population', '% of region'), (' ', 'Regional PEH'),
             (' ', 'Proportional Local PEH')])

        result_df = result_df.dropna(subset=[('GEOUID', '')])

        # Add the Total New Units
        newunits = result_df.copy()
        # Set the middle columns to null and set the Regional Population to the row title
        newunits[[('Local Population', '#'), ('Local Population', '% of region'), (' ', 'Regional PEH')]] = pd.NA
        newunits[(' ', 'Regional Population')] = 'Total New Units - 20 years'

        temp = result_df.append(newunits)
        temp = temp.sort_values(by=[("Municipality", ""), (" ", "Regional Population")])

        return temp

    @staticmethod
    def clean_table_7_data(filtered_df, year, category):
        columns = [col for col in filtered_df.columns if str(year) in col and category in col]

        df = filtered_df[columns + ['GEOUID', 'Municipality']]
        df.columns = df.columns.str.replace('PHM ', '').str.replace(f', {year}', '').str.replace(f', {category}', '')
        df.set_index(['GEOUID', 'Municipality'], inplace=True)
        transposed_df = df.T
        unstacked_df = transposed_df.unstack().reset_index()
        # pdb.set_trace()
        unstacked_df.columns = ['GEOUID', 'Municipality', f'Age – Primary Household Maintainer {year} Categories', f'{category}']
        unstacked_df = unstacked_df[~unstacked_df['Municipality'].isna()]
        unstacked_df.set_index(['GEOUID', 'Municipality'], inplace=True)
        # pdb.set_trace()
        unstacked_df.columns = pd.MultiIndex.from_tuples([(' ', f'Age – Primary Household Maintainer {year} Categories'),
                                                          (f'{year} Households', f'{category}')])
        # unstacked_df.set_index(('', f'Age – Primary Household Maintainer {year} Categories'), append=True, inplace=True)
        # pdb.set_trace()
        return unstacked_df

    @staticmethod
    def clean_table_8_data(filtered_df, year):
        columns = [col for col in filtered_df.columns if str(year) in col]
        df = filtered_df[columns + ['GEOUID', 'Municipality']]
        df.columns = df.columns.str.replace('Total Household ', '').str.replace(f', {year}', '')
        df.set_index(['GEOUID', 'Municipality'], inplace=True)
        transposed_df = df.T
        unstacked_df = transposed_df.unstack().reset_index()
        unstacked_df.columns = ['GEOUID', 'Municipality', f'Age Categories – Population', 'All Categories']
        # df = df.T.rename_axis(f'Age Categories – Population').reset_index().rename(columns={
        #     1: "All Categories"})
        # pdb.set_trace()

        new_categories = {
            '15 to 24 years': ['15 to 19 years', '20 to 24 years'],
            '25 to 34 years': ['25 to 29 years', '30 to 34 years'],
            '35 to 44 years': ['35 to 39 years', '40 to 44 years'],
            '45 to 54 years': ['45 to 49 years', '50 to 54 years'],
            '55 to 64 years': ['55 to 59 years', '60 to 64 years'],
            '65 to 74 years': ['65 to 69 years', '70 to 74 years'],
            '75 years and over': ['75 to 79 years', '80 to 84 years', '85 years and over']
        }

        summed_values_dict = {}

        # Loop through the new categories to combine and sum the values
        for new_category, old_categories in new_categories.items():
            for municipality in unstacked_df['Municipality'].unique():
                # pdb.set_trace()
                filtered_df = unstacked_df[
                    (unstacked_df['Municipality'] == municipality) & (unstacked_df['Age Categories – Population'].isin(old_categories))]
                summed_value = filtered_df['All Categories'].sum()
                if municipality not in summed_values_dict:
                    summed_values_dict[municipality] = {}
                summed_values_dict[municipality][new_category] = summed_value

            # for old_category in old_categories:
            #     summed_values_dict[old_category] = summed_value


        # Map the new combined categories to the original DataFrame
        unstacked_df['Age Categories – Household Maintainers'] = unstacked_df['Age Categories – Population'].map(
            lambda x: next((new_cat for new_cat, old_cats in new_categories.items() if x in old_cats), x))
        # pdb.set_trace()
        summed_df = pd.DataFrame(summed_values_dict).T.stack().reset_index()
        summed_df.columns = ['Municipality', 'Age Categories – Household Maintainers', 'Summed Categories']

        final_df = unstacked_df.merge(summed_df, how='left', on=['Municipality', 'Age Categories – Household Maintainers'])
        final_df = final_df[~final_df['Municipality'].isna()]
        # Map the summed values back to the original DataFrame
        final_df.set_index(['GEOUID', 'Municipality'], inplace=True)

        # pdb.set_trace()
        final_df.columns = pd.MultiIndex.from_tuples([(' ', 'Age Categories – Population'), (f'{year}', 'All Categories'),
                                                      (' ', 'Age Categories – Household Maintainers'),
                                                      (f'{year}', 'Summed Categories')
                                                      ])
        # pdb.set_trace()

        # final_df.set_index([('', 'Age Categories – Household Maintainers'),
        #                                               ('', 'Age Categories – Population')], append=True, inplace=True)
        # duplicated_mask = final_df[(f'{year}', 'Summed Categories')].duplicated()
        # # Update the duplicated values to be blank
        # final_df.loc[duplicated_mask, (f'{year}', 'Summed Categories')] = None
        # pdb.set_trace()
        return final_df

    @staticmethod
    def clean_table_9_data(filtered_df, year, category):
        columns = [col for col in filtered_df.columns if str(year) in col and category in col]
        df = filtered_df[columns + ['GEOUID', 'Municipality']]
        df.columns = df.columns.str.replace('Headship Rate ', '').str.replace(f', {year}', '').str.replace(f', {category}', '')
        df.set_index(['GEOUID', 'Municipality'], inplace=True)
        transposed_df = df.T
        unstacked_df = transposed_df.unstack().reset_index()
        unstacked_df.columns = ['GEOUID', 'Municipality', f'Age Categories – Household Maintainers', f'{category}']
        unstacked_df = unstacked_df[~unstacked_df['Municipality'].isna()]
        unstacked_df.set_index(['GEOUID', 'Municipality', 'Age Categories – Household Maintainers'], inplace=True)
        unstacked_df.columns = pd.MultiIndex.from_tuples([(f'{year} Headship Rate', f'{category}')])
        # unstacked_df.set_index(('', f'Age Categories – Household Maintainers'), append=True, inplace=True)
        # df = df.T.rename_axis(f'Age Categories – Household Maintainers')
        #
        # df.columns = [category]
        # df.columns = pd.MultiIndex.from_product([[f'{year} Headship Rate'], df.columns])
        # pdb.set_trace()
        return unstacked_df

    @staticmethod
    def clean_table_11_data(table_7_2021):
        table_7_2021[('2021 Households', 'Owner')] = table_7_2021[('2021 Households', 'Owner')].astype(str).str.replace('x', '0').astype(float)
        table_7_2021[('2021 Households', 'Renter')] = table_7_2021[('2021 Households', 'Renter')].astype(str).str.replace('x', '0').astype(float)
        row_indices_to_add = [6, 7]
        cols_to_add = [-2, -1]
        new_row = table_7_2021.reset_index(drop=True).iloc[row_indices_to_add, cols_to_add].sum(numeric_only=True, min_count=1).fillna(0)
        new_row[('Municipality', '')] = table_7_2021[('Municipality', '')].iloc[0]
        new_row[('GEOUID', '')] = table_7_2021[('GEOUID', '')].iloc[0]
        new_row[(' ', 'Age – Primary Household Maintainer 2021 Categories')] = '75 years and over'


        # Append the new row and drop the original rows
        updated_group = table_7_2021.append(new_row, ignore_index=True)
        # updated_group = updated_group.replace('75 to 84 years85 years and over', '75 years and over')
        updated_group = updated_group.drop(index=row_indices_to_add).reset_index(drop=True)
        updated_group.columns = pd.MultiIndex.from_tuples(
            [('Age Categories – Household Maintainers', '') if col == (' ', 'Age – Primary Household Maintainer 2021 Categories') else col for col in updated_group.columns])
        # pdb.set_trace()
        return updated_group

    @staticmethod
    def clean_table_12_data(filtered_df, filtered_df_cd):
        result_df = filtered_df.merge(filtered_df_cd, left_on='CD_ID', right_on='GEOUID', suffixes=('_CSD', '_CD'))
        column_order = ['GEOUID_CSD', 'Municipality', 'Regional District Projections', '2021', '2041',
                        'Regional Growth Rate']
        result_df = result_df[column_order]
        result_df.rename(columns={'GEOUID_CSD': 'GEOUID'}, inplace=True)

        return result_df

    @staticmethod
    def clean_table_13_data(filtered_df, filtered_df_cd):

        temp = filtered_df.merge(filtered_df_cd, left_on='CD_ID', right_on='GEOUID', suffixes=('_CSD', '_CD'))

        # Build regional rows
        reg = temp.copy()
        reg['Growth Scenarios'] = 'Regionally Based Household Growth'
        # pdb.set_trace()
        reg['New Units'] = (reg['Regional Growth Rate'] / 100) * reg['2021 CSD Household Estimate']
        reg['2041 Projection'] = reg['2021 CSD Household Estimate'] + reg['New Units']
        reg = reg[
            ['GEOUID_CSD', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', '2021 CSD Household Estimate',
             '2041 Projection', 'New Units']]
        reg.columns = ['GEOUID', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', 'Projection, 2021',
                       'Projection, 2041', 'New Units']

        # Build local rows
        loc = temp.copy()
        loc['Growth Scenarios'] = 'Local Household Growth'
        loc['Regional Growth Rate'] = "n/a"
        loc['New Units'] = loc['2041 CSD Household Projection'] - loc['2021 CSD Household Estimate']
        loc = loc[
            ['GEOUID_CSD', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', '2021 CSD Household Estimate',
             '2041 CSD Household Projection', 'New Units']]
        loc.columns = ['GEOUID', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', 'Projection, 2021',
                       'Projection, 2041', 'New Units']

        # Build average rows
        reg_units = reg[['GEOUID', 'New Units']]
        loc_units = loc[['GEOUID', 'New Units']]
        reg_units.set_index('GEOUID', inplace=True)
        loc_units.set_index('GEOUID', inplace=True)
        avg_df = reg[['GEOUID', 'Municipality']].copy()
        avg_df.set_index('GEOUID', inplace=True)
        avg_df['Growth Scenarios'] = 'Scenario Average'
        avg_df = avg_df.join(reg_units).join(loc_units, lsuffix='_reg', rsuffix='_loc')
        avg_df['New Units'] = avg_df[['New Units_reg', 'New Units_loc']].mean(axis=1)
        # pdb.set_trace()
        # Build total rows
        total = avg_df[['Municipality', 'New Units']].copy()
        total['Growth Scenarios'] = 'Total New Units - 20 years'
        avg_df.reset_index(inplace=True)
        total.reset_index(inplace=True)

        # Now reorganize data to match table format
        result_df = reg.append(loc).append(avg_df[['GEOUID', 'Municipality', 'Growth Scenarios', 'New Units']]).append(
            total)
        result_df = result_df.sort_values(by=['Municipality', 'Growth Scenarios'])

        return result_df

    @staticmethod
    def clean_table_14_data(filtered_df):
        bc_vacancy_rate = 0.014
        # If local rate not available, use British Columbia rate
        filtered_df.loc[filtered_df[
                            'Local primary rental market vacany rate'] == 'No data', 'Local primary rental market vacany rate'] = bc_vacancy_rate
        filtered_df['Local occupied rate'] = 1 - filtered_df['Local primary rental market vacany rate']
        filtered_df['Number of renter households in 2021'] = filtered_df['Number of renter households in 2021'].replace('x', np.nan).astype(float)
        # Create target rows
        target = filtered_df.copy()
        target[''] = 'Target Vacancy Rate'
        target = target[['GEOUID', 'Municipality', 'Local primary rental market vacany rate',
                         'Number of renter households in 2021', 'Local occupied rate', '']]
        target.columns = ['GEOUID', 'Municipality', 'Vacancy Rate',
                          'Renter Households', 'Occupied Rate', '']
        target['Vacancy Rate'] = 0.03
        target['Occupied Rate'] = 0.97
        column_order = ['GEOUID', 'Municipality', '', 'Vacancy Rate', 'Occupied Rate',
                        'Renter Households']
        target = target[column_order]

        target['Estimated Number of Units'] = target['Renter Households'] / 0.97

        # Create local rows
        local = filtered_df.copy()
        local[''] = 'Local Vacancy Rate'
        local = local[['GEOUID', 'Municipality', 'Local primary rental market vacany rate',
                       'Number of renter households in 2021', 'Local occupied rate', '']]
        local.columns = ['GEOUID', 'Municipality', 'Vacancy Rate',
                         'Renter Households', 'Occupied Rate', '']
        column_order = ['GEOUID', 'Municipality', '', 'Vacancy Rate', 'Occupied Rate',
                        'Renter Households']
        local = local[column_order]
        local['Estimated Number of Units'] = local['Renter Households'] / local['Occupied Rate']

        # Create total rows
        total = filtered_df[['GEOUID', 'Municipality']].copy()
        target_units = target[['GEOUID', 'Municipality', 'Estimated Number of Units']]
        local_units = local[['GEOUID', 'Municipality', 'Estimated Number of Units']]
        total.set_index('GEOUID', inplace=True)
        target_units.set_index('GEOUID', inplace=True)
        local_units.set_index('GEOUID', inplace=True)

        total = total.join(target_units, lsuffix='_total', rsuffix='_target').join(local_units, lsuffix='_target',
                                                                                   rsuffix='_local')
        total[''] = 'Total New Units - 20 Years'
        total['Estimated Number of Units'] = total['Estimated Number of Units_target'] - total[
            'Estimated Number of Units_local']
        total.reset_index(inplace=True)

        total = total[['GEOUID', 'Municipality_total', '', 'Estimated Number of Units']]
        total.rename(columns={'Municipality_total': 'Municipality'}, inplace=True)

        # Organize to match table format
        result_df = target.append(local).append(total)
        result_df['order'] = 2
        result_df.loc[result_df[''] == 'Target Vacancy Rate', 'order'] = 0
        result_df.loc[result_df[''] == 'Local Vacancy Rate', 'order'] = 1
        result_df = result_df.sort_values(by=['Municipality', 'order'])
        result_df = result_df.drop(columns=['order'])

        # For where the local vacancy is equal to or higher than 3%, set the needed units to 0
        geouids_to_adjust = result_df.loc[
            (result_df['Vacancy Rate'] >= 0.03) & (result_df[''] == 'Local Vacancy Rate'), 'GEOUID'].tolist()

        # Set the occupied rate to 0.97 and the Estimated Number of Units to equal the target and the total new to 0
        result_df.loc[(result_df['GEOUID'].isin(geouids_to_adjust)) & (
                    result_df[''] == 'Local Vacancy Rate'), 'Occupied Rate'] = 0.97
        result_df.loc[(result_df['GEOUID'].isin(geouids_to_adjust)) & (
                    result_df[''] == 'Local Vacancy Rate'), 'Estimated Number of Units'] = result_df.loc[(result_df[
                                                                                                               'GEOUID'].isin(
            geouids_to_adjust)) & (result_df[''] == 'Local Vacancy Rate'), 'Renter Households'] / 0.97
        result_df.loc[(result_df['GEOUID'].isin(geouids_to_adjust)) & (
                    result_df[''] == 'Total New Units - 20 Years'), 'Estimated Number of Units'] = 0

        # Set percentage fields to *100 and set renter households for local to nothing per formatting
        result_df['Vacancy Rate'] = result_df['Vacancy Rate'] * 100
        result_df['Occupied Rate'] = result_df['Occupied Rate'] * 100
        result_df.loc[result_df[''] == 'Local Vacancy Rate', 'Renter Households'] = np.nan

        return result_df

    @staticmethod
    def clean_table_16_5yr_data(filtered_df, filtered_df_cd):

        temp = filtered_df.merge(filtered_df_cd, left_on='CD_ID', right_on='GEOUID', suffixes=('_CSD', '_CD'))

        # Build regional rows
        reg = temp.copy()
        reg['Growth Scenarios'] = 'Regionally Based Household Growth'
        reg['New Units'] = (reg['Regional Growth Rate'] / 100) * reg['2021 CSD Household Estimate']
        reg['2026 Projection'] = reg['2021 CSD Household Estimate'] + reg['New Units']
        reg = reg[
            ['GEOUID_CSD', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', '2021 CSD Household Estimate',
             '2026 Projection', 'New Units']]
        reg.columns = ['GEOUID', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', 'Projection, 2021',
                       'Projection, 2026', 'New Units']

        # Build local rows
        loc = temp.copy()
        loc['Growth Scenarios'] = 'Local Household Growth'
        loc['Regional Growth Rate'] = "n/a"
        loc['New Units'] = loc['2026 CSD Household Projection'] - loc['2021 CSD Household Estimate']
        loc = loc[
            ['GEOUID_CSD', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', '2021 CSD Household Estimate',
             '2026 CSD Household Projection', 'New Units']]
        loc.columns = ['GEOUID', 'Municipality', 'Growth Scenarios', 'Regional Growth Rate', 'Projection, 2021',
                       'Projection, 2026', 'New Units']

        # Build average rows
        reg_units = reg[['GEOUID', 'New Units']]
        loc_units = loc[['GEOUID', 'New Units']]
        reg_units.set_index('GEOUID', inplace=True)
        loc_units.set_index('GEOUID', inplace=True)
        avg_df = reg[['GEOUID', 'Municipality']].copy()
        avg_df.set_index('GEOUID', inplace=True)
        avg_df['Growth Scenarios'] = 'Scenario Average'
        avg_df = avg_df.join(reg_units).join(loc_units, lsuffix='_reg', rsuffix='_loc')
        avg_df['New Units'] = avg_df[['New Units_reg', 'New Units_loc']].mean(axis=1)

        # Build total rows
        total = avg_df[['Municipality', 'New Units']].copy()
        total['Growth Scenarios'] = 'Total New Units - 5 years'
        avg_df.reset_index(inplace=True)
        total.reset_index(inplace=True)

        # Now reorganize data to match table format
        result_df = reg.append(loc).append(avg_df[['GEOUID', 'Municipality', 'Growth Scenarios', 'New Units']]).append(
            total)
        result_df = result_df.sort_values(by=['Municipality', 'Growth Scenarios'])

        return result_df




    @staticmethod
    def clean_input_data(input_df):
        clean_input = input_df.copy()
        new_columns = []
        for col in clean_input.columns:
            new_col = tuple('' if 'Unnamed' in str(part) else part for part in col)
            new_columns.append('_'.join([str(part).strip() for part in new_col if part != '']))
        clean_input.columns = new_columns
        # pdb.set_trace()
        # input_df.columns = input_df.columns.map('_'.join).str.strip('_')
        return clean_input


    @staticmethod
    def apply_formula(input_df, formula_df):
        clean_input_df = input_df.copy()
        clean_formula_df = formula_df.copy()
        clean_formula_df['Numerator Indices'] = clean_formula_df['Numerator'].apply(lambda x: [int(i) + 3 for i in str(x).split(',')])
        clean_formula_df['Denominator Indices'] = clean_formula_df['Denominator'].apply(
            lambda x: [int(i) + 3 for i in str(x).split(',') if x is not None] if pd.notna(x) else []
        )

        results_df = pd.DataFrame(index=clean_input_df.index)
        for _, row in clean_formula_df.iterrows():
            numerator_indices = row['Numerator Indices']
            denominator_indices = row['Denominator Indices']
            formula_class = row['Formula Class']
            output_column = row['Output']
            # pdb.set_trace()
            numerator_values = clean_input_df.iloc[:, numerator_indices].sum(axis=1)
            try:
                denominator_values = clean_input_df.iloc[:, denominator_indices].sum(axis=1)
            except ValueError:
                denominator_values = 0
            # pdb.set_trace()


            result = pd.Series([None] * len(clean_input_df), index=clean_input_df.index)
            valid_mask = (denominator_values != 0) & denominator_values.apply(lambda x: isinstance(x, (int, float)))
            if formula_class == 1:
                result[valid_mask] = (numerator_values[valid_mask] / denominator_values[valid_mask]) * 100
                # pdb.set_trace()
                result[valid_mask] = result[valid_mask].astype(str) + "%"

            elif formula_class == 2:
                result[valid_mask] = (numerator_values[valid_mask] / denominator_values[valid_mask]) * denominator_values[valid_mask]

            elif formula_class == 3:
                result = numerator_values
            else:
                result = None  # Handle other formula classes if needed

            # pdb.set_trace()
            results_df[output_column] = result

        return pd.concat([clean_input_df, results_df], axis=1)


