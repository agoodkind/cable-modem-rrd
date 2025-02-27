// A union of table names for use in the discriminant
export const tableNames = [
    "downstream_bonded_channels",
    "upstream_bonded_channels",
    "downstream_ofdma_channels",
    "upstream_ofdma_channels",
] as const;

export type TableName = (typeof tableNames)[number];

// Common type aliases
export type LockedStatus = "Locked" | "Not Locked";
export type Modulation = "QAM256" | "Unknown";
export type ChannelType = "ATDMA" | "Unknown";

export interface CommonChannelFields {
    channel: number;
    channelId: number;
    frequency: number;
    lockedStatus: LockedStatus;
    power: number;
    timestamp: number;
    id: string;
} // --- Channel Interfaces ---

// Downstream bonded channel
export interface DownstreamBondedChannel extends CommonChannelFields {
    correctables: number;
    modulation: Modulation;
    snr: number;
    uncorrectables: number;
}

// Upstream bonded channel
export interface UpstreamBondedChannel extends CommonChannelFields {
    channelType: ChannelType;
    frequency: number;
    symbolRate: number;
}

// Downstream OFDMA channel
export interface DownstreamOfdmaChannel extends CommonChannelFields {
    activeSubcarrier1: number;
    activeSubcarrier2: number;
    correctable: number;
    profileId: string;
    snr: number;
    incorrectable: number;
    inerror: number;
}

// Upstream OFDMA channel
export interface UpstreamOfdmaChannel extends CommonChannelFields {
    frequency: number;
    profileId: string;
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
