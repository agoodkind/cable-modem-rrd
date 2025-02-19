// A union of table names for use in the discriminant
export const tableNames = [
  "downstream_bonded_channels",
  "upstream_bonded_channels",
  "downstream_ofdma_channels",
  "upstream_ofdma_channels",
] as const;

export type TableName = typeof tableNames[number];

// Common type aliases
export type LockedStatus = "Locked" | "Not Locked";
export type Modulation = "QAM256" | "Unknown";
export type ChannelType = "ATDMA" | "Unknown";

// --- Channel Interfaces ---

// Downstream bonded channel
export interface DownstreamBondedChannel {
  Channel: number;
  ChannelID: number;
  Correctables: number;
  Frequency: number;
  LockedStatus: LockedStatus;
  Modulation: Modulation;
  Power: number;
  SNR: number;
  Uncorrectables: number;
  timestamp: number;
}

// Upstream bonded channel
export interface UpstreamBondedChannel {
  Channel: number;
  ChannelID: number;
  ChannelType: ChannelType;
  Frequency: number;
  LockedStatus: LockedStatus;
  Power: number;
  SymbolRate: number;
  timestamp: number;
}

// Downstream OFDMA channel
export interface DownstreamOfdmaChannel {
  ActiveSubcarrier1: number;
  ActiveSubcarrier2: number;
  Channel: number;
  ChannelID: number;
  Correctable: number;
  Frequency: number;
  LockedStatus: LockedStatus;
  Power: number;
  ProfileID: string;
  "SNR/MER": number;
  Uncorrectable: number;
  Unerror: number;
  timestamp: number;
}

// Upstream OFDMA channel
export interface UpstreamOfdmaChannel {
  Channel: number;
  ChannelID: number;
  Frequency: number;
  LockedStatus: LockedStatus;
  Power: number;
  ProfileID: string;
  timestamp: number;
}

// --- Discriminated Union Wrappers ---

export interface DownstreamBondedTable {
  tableName: "downstream_bonded_channels";
  data: DownstreamBondedChannel[];
}

export interface UpstreamBondedTable {
  tableName: "upstream_bonded_channels";
  data: UpstreamBondedChannel[];
}

export interface DownstreamOfdmaTable {
  tableName: "downstream_ofdma_channels";
  data: DownstreamOfdmaChannel[];
}

export interface UpstreamOfdmaTable {
  tableName: "upstream_ofdma_channels";
  data: UpstreamOfdmaChannel[];
}

export type TableData =
  | DownstreamBondedChannel
  | UpstreamBondedChannel
  | DownstreamOfdmaChannel
  | UpstreamOfdmaChannel;

export type TableDataColumn = keyof TableData;
export type AllPossibleTableDataColumns = keyof DownstreamBondedChannel &
  keyof UpstreamBondedChannel &
  keyof DownstreamOfdmaChannel &
  keyof UpstreamOfdmaChannel;

// The union that lets you narrow based on tableName
export type Table =
  | DownstreamBondedTable
  | UpstreamBondedTable
  | DownstreamOfdmaTable
  | UpstreamOfdmaTable;

// The overall response is an array of each table type.
export type CableModemData = Table[];
