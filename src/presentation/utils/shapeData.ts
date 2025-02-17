import type { TableData } from "../dataTypes";
export type TShapedData<T extends TableData> = { [timestamp: number]: T[] };

export const shapeData = <T extends TableData = TableData>(
  data: T[],
): TShapedData<T> => {
  return data.reduce(
    (acc, row) => {
      if (!acc[row.timestamp]) {
        acc[row.timestamp] = [];
      }
      acc[row.timestamp].push(row);
      return acc;
    },
    {} as { [timestamp: number]: T[] },
  );
};

// based on ChannelID get max and min channel and use that to set the domain
export const getChannelDomain = (data: TableData[]) => {
  const channelIDs = data.map((d) => d.ChannelID);
  return [Math.min(...channelIDs), Math.max(...channelIDs)];
};
