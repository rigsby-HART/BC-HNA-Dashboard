import pdb

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from PrepareTables import PrepareTables


class DBUploader:
    def __init__(self, master_csd_data, master_cd_data, formulas_data, db_path):
        self.master_csd_data = master_csd_data
        self.master_cd_data = master_cd_data
        self.formulas_data = formulas_data
        self.db_path = db_path
        # pdb.set_trace()
        self.engine = create_engine('sqlite:///' + self.db_path)
        self.pt = PrepareTables(master_csd_data, master_cd_data, formulas_data)
        self.db_base = declarative_base()
        self.upload_tables()
        self.Session = sessionmaker(bind=self.engine)

    def __call__(self):

        # self.insert_data(self.id_table, self.Id_Table)
        # Preparing Section A
        self.insert_data(self.table_4a_new, self.Table_4a)
        self.insert_data(self.table_4b_new, self.Table_4b)
        self.insert_data(self.table_5_new, self.Table_5)

        # Preparing Section B
        self.insert_data(self.table_6_new, self.Table_6)

        # Preparing Section C
        self.insert_data(self.table_7_2006_new, self.Table_7_2006)
        self.insert_data(self.table_7_2021_new, self.Table_7_2021)
        self.insert_data(self.table_8_new, self.Table_8)
        self.insert_data(self.table_9_new, self.Table_9)
        self.insert_data(self.table_10_new, self.Table_10)
        self.insert_data(self.table_11_new, self.Table_11)

        # Preparing Section D
        self.insert_data(self.table_12_new, self.Table_12)
        self.insert_data(self.table_13_new, self.Table_13)

        # Preparing Section E
        self.insert_data(self.table_14_new, self.Table_14)

        # Preparing Section F
        self.insert_data(self.table_15_new, self.Table_15)

        # Preparing Section G
        self.insert_data(self.table_16_new, self.Table_16)

        print('Database ready....')


    def upload_tables(self):
        # class Id_Table(self.db_base):
        #     __tablename__ = "id_table"
        #     self.id_table = pd.read_excel('..\\inputs\\Id_file.xlsx')
        #     print(self.id_table[1:])
        #
        #     # self.id_table.columns = ['_'.join(col).strip() for col in self.id_table.columns]
        #     pdb.set_trace()
        #
        #     # Define your primary key
        #     GEOID = Column(Integer, primary_key=True, comment='primary key')
        #
        #     # Dynamically add columns based on the DataFrame columns
        #     for col in self.id_table.columns:
        #         if col == 'GEODID':
        #             continue
        #         elif col == 'CD_ID':
        #             vars()[col] = Column(Integer)
        #         else:
        #             vars()[col] = Column(String)
        #
        # self.Id_Table = Id_Table  # Save the class to use later

        class Table_4a(self.db_base):
            __tablename__ = "table_4a_new"
            self.table_4a, _ = self.pt.prepare_table_4()
            # print(self.table_4a.columns)
            # pdb.set_trace()
            self.table_4a_new = self.table_4a.replace('x', np.nan)
            self.table_4a_new.columns = self.table_4a_new.columns.map(str)
            # print(self.table_4a_new, self.table_4a_new.dtypes)
            # pdb.set_trace()
            # self.table_4a_new.columns = ['_'.join(col).strip() for col in self.table_4a_new.columns]

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_4a_new.columns:
                if (col == 'Municipality') | (col == 'Total Households') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)
            # pdb.set_trace()

        self.Table_4a = Table_4a  # Save the class to use later

        class Table_4b(self.db_base):
            __tablename__ = "table_4b_new"
            _, self.table_4b = self.pt.prepare_table_4()
            self.table_4b_new = self.table_4b.replace('x', np.nan)
            # print(self.table_4b_new.columns)
            self.table_4b_new.columns = ['_'.join(map(str, col)).strip() for col in self.table_4b_new.columns]
            # print(self.table_4b_new.columns)
            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_4b_new.columns:
                if (col == 'Municipality_') | (col == '_Extreme Core Housing Need') | (
                        col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_4b = Table_4b  # Save the class to use later

        class Table_5(self.db_base):
            __tablename__ = "table_5_new"
            self.table_5 = self.pt.prepare_table_5(self.table_4b)
            self.table_5_new = self.table_5.replace('x', np.nan)
            # self.table_5_new.columns = ['_'.join(col).strip() for col in self.table_5_new.columns]

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_5_new.columns:
                if (col == 'Municipality') | (col == 'Total Households') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_5 = Table_5  # Save the class to use later

        class Table_6(self.db_base):
            __tablename__ = "table_6_new"
            self.table_6 = self.pt.prepare_table_6()
            self.table_6_new = self.table_6.replace('x', np.nan)
            self.table_6_new.columns = ['_'.join(col).strip() for col in self.table_6_new.columns]

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_6_new.columns:
                if (col == 'Municipality_') | (col == '_Regional Population') | (
                        col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_6 = Table_6  # Save the class to use later

        class Table_7_2006(self.db_base):
            __tablename__ = "table_7_2006_new"
            self.table_7_2006, _ = self.pt.prepare_table_7()
            self.table_7_2006_new = self.table_7_2006.copy()
            self.table_7_2006_new.columns = ['_'.join(col).strip() for col in self.table_7_2006_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_7_2006_new.columns:
                if (col == 'Municipality_') | (col == '_Age – Primary Household Maintainer 2006 Categories') | (
                        col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        # pdb.set_trace()
        # print(self.table_7_2006_new.dtypes)
        self.Table_7_2006 = Table_7_2006  # Save the class to use later

        class Table_7_2021(self.db_base):
            __tablename__ = "table_7_2021_new"
            _, self.table_7_2021 = self.pt.prepare_table_7()
            self.table_7_2021_new = self.table_7_2021.replace('x', np.nan)
            self.table_7_2021_new.columns = ['_'.join(col).strip() for col in self.table_7_2021_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_7_2021_new.columns:
                if (col == 'Municipality_') | (col == '_Age – Primary Household Maintainer 2021 Categories') | (
                        col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Integer)

        self.Table_7_2021 = Table_7_2021  # Save the class to use later

        class Table_8(self.db_base):
            __tablename__ = "table_8_new"
            self.table_8 = self.pt.prepare_table_8()
            self.table_8_new = self.table_8.replace('x', np.nan).replace('xx', np.nan).reset_index()
            self.table_8_new.columns = ['_'.join(col).strip() for col in self.table_8_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_8_new.columns:
                if (col == 'Municipality_') | (col == '_Age Categories – Household Maintainers') | \
                        (col == '_Age Categories – Population') | (col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Integer)
        # pdb.set_trace()
        self.Table_8 = Table_8  # Save the class to use later

        class Table_9(self.db_base):
            __tablename__ = "table_9_new"
            self.table_9, _ = self.pt.prepare_table_9_10(self.table_7_2006, self.table_8)
            self.table_9_new = self.table_9.replace('x', np.nan)
            self.table_9_new.columns = ['_'.join(col).strip() for col in self.table_9_new.columns]
            self.table_9_new['2006 Headship Rate_Owner'] = self.table_9_new['2006 Headship Rate_Owner'].str.rstrip('%').astype(float) / 100.0
            self.table_9_new['2006 Headship Rate_Renter'] = self.table_9_new['2006 Headship Rate_Renter'].str.rstrip('%').astype(float) / 100.0
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_9_new.columns:
                if (col == 'Municipality_') | (col == '_Age Categories – Household Maintainers') | (col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_9 = Table_9  # Save the class to use later

        class Table_10(self.db_base):
            __tablename__ = "table_10_new"
            _, self.table_10 = self.pt.prepare_table_9_10(self.table_7_2006, self.table_8)
            self.table_10_new = self.table_10.replace('x', np.nan)
            self.table_10_new.columns = ['_'.join(col).strip() for col in self.table_10_new.columns]
            self.table_10_new['2006 Headship Rate_Owner'] = self.table_10_new['2006 Headship Rate_Owner'].str.rstrip('%').astype(float) / 100.0
            self.table_10_new['2006 Headship Rate_Renter'] = self.table_10_new['2006 Headship Rate_Renter'].str.rstrip('%').astype(float) / 100.0
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_10_new.columns:
                if (col == 'Municipality_') | (col == '_Age Categories – Household Maintainers') | (col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_10 = Table_10  # Save the class to use later

        class Table_11(self.db_base):
            __tablename__ = "table_11_new"
            self.table_11 = self.pt.prepare_table_11(self.table_7_2021, self.table_10)
            self.table_11_new = self.table_11.replace('x', np.nan)
            self.table_11_new.columns = ['_'.join(col).strip() for col in self.table_11_new.columns]
            # self.table_11['2006 Headship Rate_Owner'] = self.table_11['2006 Headship Rate_Owner'].str.rstrip('%').astype(float) / 100.0
            # self.table_11['2006 Headship Rate_Renter'] = self.table_11['2006 Headship Rate_Renter'].str.rstrip('%').astype(float) / 100.0
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_11_new.columns:
                if (col == 'Municipality_') | (col == '_Age Categories – Household Maintainers') | (col == 'GEOID_'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_11 = Table_11  # Save the class to use later

        class Table_12(self.db_base):
            __tablename__ = "table_12_new"
            self.table_12, _ = self.pt.prepare_table_12_13()
            self.table_12_new = self.table_12.replace('x', np.nan)
            # self.table_12_new.columns = ['_'.join(col).strip() for col in self.table_12_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_12_new.columns:
                if (col == 'Municipality') | (col == 'Regional District Projections') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_12 = Table_12  # Save the class to use later


        class Table_13(self.db_base):
            __tablename__ = "table_13_new"
            _, self.table_13 = self.pt.prepare_table_12_13()
            self.table_13_new = self.table_13.replace('x', np.nan)
            self.table_13_new.columns = ['_'.join(col).strip() for col in self.table_13_new.columns]
            self.table_13_new['Regional Growth Rate_'] = self.table_13_new['Regional Growth Rate_'].replace('n/a', np.nan).astype(float)
            # self.table_12_new.columns = ['_'.join(col).strip() for col in self.table_12_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_13_new.columns:
                if (col == 'Municipality_') | (col == 'Growth Scenarios_') | (
                        col == 'GEOID_'):
                    vars()[col] = Column(String)
                elif (col == 'New Units_') | (col == 'Demand factor_'):
                    vars()[col] = Column(Float)
                else:
                    vars()[col] = Column(Integer)

        self.Table_13 = Table_13  # Save the class to use later


        class Table_14(self.db_base):
            __tablename__ = "table_14_new"
            self.table_14 = self.pt.prepare_table_14()
            self.table_14_new = self.table_14.replace('x', np.nan)
            self.table_14_new = self.table_14_new.rename(columns={'': 'Remove this column name'})
            # self.table_12_new.columns = ['_'.join(col).strip() for col in self.table_12_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_14_new.columns:
                if (col == 'Municipality') | (col == 'Remove this column name') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                elif col == 'Estimated Number of Units':
                    vars()[col] = Column(Float)
                else:
                    vars()[col] = Column(Integer)

        self.Table_14 = Table_14  # Save the class to use later

        class Table_15(self.db_base):
            __tablename__ = "table_15_new"
            self.table_15 = self.pt.prepare_table_15(self.table_5, self.table_6, self.table_11, self.table_14)
            self.table_15_new = self.table_15.replace('x', np.nan)
            # self.table_12_new.columns = ['_'.join(col).strip() for col in self.table_12_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_15_new.columns:
                if (col == 'Municipality') | (col == 'Component') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Integer)

        self.Table_15 = Table_15  # Save the class to use later


        class Table_16(self.db_base):
            __tablename__ = "table_16_new"
            self.table_16 = self.pt.prepare_table_16(self.table_5, self.table_6, self.table_11, self.table_13, self.table_14, self.table_15)
            self.table_16_new = self.table_16.replace('x', np.nan)
            # self.table_12_new.columns = ['_'.join(col).strip() for col in self.table_12_new.columns]
            # pdb.set_trace()

            # Define your primary key
            pk = Column(Integer, primary_key=True, comment='primary key')

            # Dynamically add columns based on the DataFrame columns
            for col in self.table_16_new.columns:
                if (col == 'Municipality') | (col == 'Component') | (
                        col == 'GEOID'):
                    vars()[col] = Column(String)
                else:
                    vars()[col] = Column(Float)

        self.Table_16 = Table_16  # Save the class to use later

        # Create all tables
        self.db_base.metadata.create_all(self.engine)

    def insert_data(self, df, PartnerClass):
        # Create a new session
        session = self.Session()

        # Iterate through the DataFrame and insert data
        for idx, row in df.iterrows():
            data = row.to_dict()
            partner_instance = PartnerClass(**data)
            session.add(partner_instance)

        # Commit the transaction
        #     try:
        session.commit()
            # except IntegrityError as e:
            #     session.rollback()
            #     print(f"Error at row {idx}: {e}")
            #     print(f"Row data: {data}")
        session.close()


