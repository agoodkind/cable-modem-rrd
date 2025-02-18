import { useState } from "react";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { TableData, TableDataColumn } from "../dataTypes";
import { shapeData } from "../utils/shapeData";
import { ChartTooltip } from "./ChartToolTip";

const getDefaultColumn = (data: TableData[]) => {
  if ("SNR" in data[0]) {
    return "SNR";
  } else if ("SNR/MER" in data[0]) {
    return "SNR/MER";
  } else {
    return "Power";
  }
};

function Graph({ data }: { data: TableData[] }) {
  const [selectedColumn, setSelectedColumn] = useState<TableDataColumn>(
    getDefaultColumn(data) as TableDataColumn,
  );
  const shapedData = shapeData(data);

  const channelMapping = Object.entries(shapedData).map(
    ([timestamp, tableData]) => {
      const collector: any = {};

      tableData.forEach((tableDataEntry) => {
        // if table has SNR
        collector[`channel_${tableDataEntry.ChannelID}`] =
          tableDataEntry[selectedColumn];
      });

      return {
        timestamp,
        ...collector,
      };
    },
  );

  const maxSelectedColumnValue = Math.max(
    ...(data.map((d) => d[selectedColumn]) as number[]),
  );
  const minSelectedColumnValue = Math.min(
    ...(data.map((d) => d[selectedColumn]) as number[]),
  );

  const columnNames = Object.keys(data[0]) as TableDataColumn[];
  const channelGroupLength = Object.entries(shapedData)[0][1].length;

  return (
    <>
      <select
        className="w-fit rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
        value={selectedColumn ?? getDefaultColumn(data)}
        onChange={(e) =>
          setSelectedColumn(e.currentTarget.value as TableDataColumn)
        }
      >
        {columnNames.map((key) => (
          <option value={key} key={key} selected={key === selectedColumn}>
            {key}
          </option>
        ))}
      </select>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={channelMapping} className="text-black dark:text-white">
          {Array.from(Array(channelGroupLength)).map((_, index) => {
            return (
              <Line
                type="monotone"
                key={index}
                name={`Channel ${index}`}
                dataKey={`channel_${index}`}
                stroke={`#${Math.floor(Math.random() * 16777215).toString(16)}`}
              />
            );
          })}

          <XAxis
            dataKey={(data) => {
              const date = new Date(Number(data.timestamp) * 1000);
              return date.toLocaleTimeString();
            }}
            hide={true}
          />
          <YAxis
            scale="linear"
            domain={[minSelectedColumnValue, maxSelectedColumnValue]}
          />
          <Tooltip content={ChartTooltip} />
        </LineChart>
      </ResponsiveContainer>
    </>
  );
}

export default Graph;
