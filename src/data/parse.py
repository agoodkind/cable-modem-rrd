# %%
import pandas as pd
import sqlite3
from datetime import datetime
import re
from dataclasses import dataclass
from flask import Flask
from vars import sqlconn, cable_info_file

# %%
@dataclass
class CableData:
    # general_status: Dict[str, str]
    # startup_procedure: Dict[str, str]
    downstream_bonded_channels: pd.DataFrame
    upstream_bonded_channels: pd.DataFrame
    downstream_ofdma_channels: pd.DataFrame
    upstream_ofdma_channels: pd.DataFrame
    # event_log: pd.DataFrame

content = cable_info_file().read()


# # Parse General Status
# status_section = content.split('Startup Procedure')[0]
# status_matches = re.findall(r'([\w\s]+Status(?:[^:]+)?): ([\w\s]+)', status_section)
# general_status = {k.strip(): v.strip() for k, v in status_matches}

# # Parse Startup Procedure
# startup_section = content.split('Startup Procedure')[1].split('Downstream Bonded Channels')[0]
# startup_procedure = {}
# for line in startup_section.strip().split('\n'):
#     if ':' in line:
#         key, value = line.split(':', 1)
#         startup_procedure[key.strip()] = value.strip()


# %%
# to data frame
def parse_section_into_df(section: str) -> pd.DataFrame:
    lines = [line.strip() for line in section.split('\n') if line.strip()]
    
    columns = re.split(r'\s+', lines[0])
    data = [re.sub(r'\s{2,}', ',',  line).split(',') for line in lines[1:]]

    df = pd.DataFrame(data=data, columns=columns)
    df["timestamp"] = int(datetime.now().timestamp())
    df["Channel"] = df["Channel"].astype(int)
    df["ChannelID"] = df["ChannelID"].astype(int)

    df["Frequency"] = df["Frequency"].str.replace("Hz", "").astype(int)
    df["Power"] = df["Power"].str.replace("dBmV", "").astype(float)

    if "Correctables" in df.columns:
        df["Correctables"] = df["Correctables"].astype(int)
        
    if "Uncorrectables" in df.columns:
        df["Uncorrectables"] = df["Uncorrectables"].astype(int)

    if "SNR" in df.columns:
        df["SNR"] = df["SNR"].astype(float)

    if "SymbolRate" in df.columns:
        df["SymbolRate"] = df["SymbolRate"].str.replace("Ksym/sec", "").astype(int)

    return df

# %%
def parse_odfma_downstream_section_custom(section: str) -> pd.DataFrame:
    """
        this exists because netgear and xfinity hates us
    """
#Downstream OFDM Channels
#Channel   LockedStatus  ProfileID  ChannelID    Frequency       Power       SNR/MER    ActiveSubcarrier    Unerror    Correctable   Uncorrectable
    # 1     Locked     0 ,1 ,2 ,3     45     850000000 Hz     -0.02 dBmV     40.1 dB     1108 ~ 2987     7712810     7483251     0
    # => ["1", "Locked", "0 ,1 ,2 ,3", "45", "850000000 Hz", "-0.02 dBmV", "40.1 dB", "1108 ~ 2987", "7712810", "7483251", "0"]
    lines = [line.strip() for line in section.split('\n') if line.strip()]

    columns_unclean = re.sub(r'ActiveSubcarrier', 'ActiveSubcarrier1 ActiveSubcarrier2', lines[0])
    columns = re.split(r'\s+', columns_unclean)
    data = [
        re.sub(r'\s{2,}|~', '|',  line).split('|')
        for line in lines[1:]
    ]

    # def get_profile_id_range(line): 
    #     return len(line) - len(columns) - 1

    # def parse_line(line): 
    #     return line[:2] + [','.join(line[2:get_profile_id_range(line)])] + line[get_profile_id_range(line):]

    # data = [
    #     parse_line(line)
    #     for line in data_unclean
    # ]

    df = pd.DataFrame(data=data, columns=columns)
    df["Channel"] = df["Channel"].astype(int)
    df["ChannelID"] = df["ChannelID"].astype(int)
    df["Frequency"] = df["Frequency"].replace(r'Hz', '', regex=True).astype(int)
    df["Power"] = df["Power"].replace(r'dBmV', '', regex=True).astype(float)
    df["SNR/MER"] = df["SNR/MER"].replace(r'dB', '', regex=True).astype(float)
    df["ActiveSubcarrier1"] = df["ActiveSubcarrier1"].astype(int)
    df["ActiveSubcarrier2"] = df["ActiveSubcarrier2"].astype(int)
    df["Unerror"] = df["Unerror"].astype(int)
    df["Correctable"] = df["Correctable"].astype(int)
    df["Uncorrectable"] = df["Uncorrectable"].astype(int)
    df["timestamp"] = int(datetime.now().timestamp())
    
    return df
    

# %%

# Parse Event Log
event_section = content.split('Event Log')[1]
event_pattern = r'((?:Time Not Established|[\w\s]+\d{2}:\d{2}:\d{2}\s+\d{4}))\s+(\w+\s+\(\d+\))\s+(.+?)(?=(?:Time Not Established|[\w\s]+\d{2}:\d{2}:\d{2}\s+\d{4})|$)'
events = re.findall(event_pattern, event_section, re.DOTALL)
event_df = pd.DataFrame(events, columns=['Timestamp', 'Priority', 'Description'])


# %%
downstream_section = content.split('Downstream Bonded Channels')[1].split('Upstream Bonded Channels')[0]
upstream_section = content.split('Upstream Bonded Channels')[1].split('Downstream OFDM Channels')[0]
ofdma_downstream_section = content.split('Downstream OFDM Channels')[1].split('Upstream OFDMA Channels')[0]
ofdma_upstream_section = content.split('Upstream OFDMA Channels')[1].split('Event Log')[0]





# %%
# Initialize database

# create_tables(conn)

# Parse file
# cable_data = parse_file('')

# # Insert data using pandas to_sql
# pd.DataFrame([cable_data.general_status.items()], 
#             columns=['status_type', 'status_value']).to_sql(
#     'general_status', conn, if_exists='replace', index=False
# )

# pd.DataFrame([cable_data.startup_procedure.items()], 
#             columns=['parameter', 'value']).to_sql(
#     'startup_procedure', conn, if_exists='replace', index=False
# )

cable_data = CableData(
    downstream_bonded_channels=parse_section_into_df(downstream_section),
    upstream_bonded_channels=parse_section_into_df(upstream_section),
    downstream_ofdma_channels=parse_odfma_downstream_section_custom(ofdma_downstream_section),
    upstream_ofdma_channels=parse_section_into_df(ofdma_upstream_section),
    # event_log=event_df
)
with sqlconn() as conn:

    cable_data.downstream_bonded_channels.to_sql(
        'downstream_bonded_channels', conn, if_exists='append', index=False
    )

    cable_data.upstream_bonded_channels.to_sql(
        'upstream_bonded_channels', conn, if_exists='append', index=False
    )

    cable_data.downstream_ofdma_channels.to_sql(
        'downstream_ofdma_channels', conn, if_exists='append', index=False
    )

    cable_data.upstream_ofdma_channels.to_sql(
        'upstream_ofdma_channels', conn, if_exists='append', index=False
    )

    conn.commit()

