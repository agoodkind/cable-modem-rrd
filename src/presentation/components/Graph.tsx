import { useState } from "react";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  type TooltipProps,
} from "recharts";
import type {
  NameType,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";
import type { TableData, TableDataColumn } from "../dataTypes";
import { shapeData } from "../utils/shapeData";

const getDefaultColumn = (data: TableData[]) => {
  if (!data.length) {
    return "Power";
  }
  if ("SNR" in data[0]) {
    return "SNR";
  } else if ("SNR/MER" in data[0]) {
    return "SNR/MER";
  } else {
    return "Power";
  }
};

const ChartTooltip = ({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) => {
  if (!active || !payload || !payload.length) {
    return null;
  }
  return (
    <div className="grid max-h-80 gap-2 rounded bg-white p-2 dark:bg-gray-800">
      <div className="text-lg font-bold">{label}</div>
      <ul className="grid grid-cols-4 text-sm font-normal">
        {payload
          .sort((a, b) => {
            return Number(b.value) - Number(a.value);
          })
          .map((entry, index) => (
            <li key={`item-${index}`}>{`${entry.name}: ${entry.value}`}</li>
          ))}
      </ul>
    </div>
  );
};

const randomHexColors = [
  "#AAD04E",
  "#F2C2AB",
  "#ADD949",
  "#C3BE07",
  "#CAE370",
  "#2189BF",
  "#9E88A7",
  "#A26283",
  "#651355",
  "#4BC755",
  "#6BC0DE",
  "#8C621D",
  "#02BB21",
  "#D3C1A7",
  "#2C6B3A",
  "#F7EA47",
  "#364A1C",
  "#E82E7B",
  "#FB37DA",
  "#7186CD",
  "#802C09",
  "#D408DD",
  "#1F168D",
  "#B07AD5",
  "#2F5938",
  "#D06E65",
  "#BC649C",
  "#EFC3C6",
  "#D96B67",
  "#1CAD91",
  "#97EF70",
  "#545565",
];

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
        collector[`channel_${tableDataEntry.Channel}`] =
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

  // const minSelectedColumnValue = Math.min(
  //   ...(data.map((d) => d[selectedColumn]) as number[]),
  // );
  // get min non-zero value
  const minSelectedColumnValue = Math.min(
    ...(data
      .map((d) => d[selectedColumn])
      .filter((v) => Number(v) > 0) as number[]),
  );

  if (!data.length) {
    return <div>No data available</div>;
  }

  const columnNames = Object.keys(data[0]) as TableDataColumn[];
  const channelGroupLength = Object.entries(shapedData)[0][1].length;

  return (
    <>
      <select
        className="w-fit rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
        value={selectedColumn ?? getDefaultColumn(data)}
        defaultValue={getDefaultColumn(data)}
        onChange={(e) =>
          setSelectedColumn(e.currentTarget.value as TableDataColumn)
        }
      >
        {columnNames.map((key) => (
          <option value={key} key={key}>
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
                stroke={randomHexColors[index]}
                dot={false}
              />
            );
          })}
          <XAxis
            dataKey={(data) => {
              const date = new Date(Number(data.timestamp) * 1000);
              return date.toString();
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
