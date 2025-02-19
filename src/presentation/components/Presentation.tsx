import { useCallback, useEffect, useState } from "react";
import type { CableModemData, Table, TableName } from "../dataTypes";
import Graph from "./Graph";

const listTables = async (): Promise<TableName[]> => {
  const response = await fetch("/api/tables");
  const data: string[] = await response.json();
  return data.reverse() as TableName[];
};

const loadTables = async (
  minTs: number,
  maxTs: number,
): Promise<CableModemData> => {
  const tables = await listTables();
  const tableDataMapPromises = tables.map(async (table) => {
    const qParams = new URLSearchParams({
      min_ts: Math.floor(minTs / 1000).toString(),
      max_ts: Math.floor(maxTs / 1000).toString(),
    });
    const response = await fetch(`/api/tables/${table}?${qParams}`);
    const data = await response.json();
    // Create the discriminated object:
    return { tableName: table as TableName, data } as Table;
  });

  return await Promise.all(tableDataMapPromises);
};

function Presentation() {
  const [tableData, setTableData] = useState<CableModemData>();
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [minTimestamp, setMinTimestamp] = useState<number>(
    Date.now() - 1000 * 60 * 60 * 1,
  ); // past hour
  const [maxTimestamp, setMaxTimestamp] = useState<number>(Date.now());
  const [refreshEnabled, setRefreshEnabled] = useState(false);

  const reloadData = useCallback(async () => {
    if (busy) {
      return;
    }

    try {
      const tableData = await loadTables(minTimestamp, maxTimestamp);
      setTableData(tableData);
      setError(null);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError(JSON.stringify(error));
      }
    } finally {
      setBusy(false);
    }
  }, [minTimestamp, maxTimestamp]);

  useEffect(() => {
    reloadData();
  }, [reloadData, minTimestamp, maxTimestamp]);

  useEffect(() => {
    if (refreshEnabled) {
      const intervalId = setInterval(() => {
        reloadData();
      }, 1000 * 60 * 5); // 5 minutes
      return () => clearInterval(intervalId);
    }
  }, [refreshEnabled, reloadData]);

  return (
    <main className="fixed h-[100vh] w-[100vw] overflow-auto dark:bg-gray-800 dark:text-white">
      <div className="flex flex-col gap-10 overflow-auto p-10">
        {error ? <span className="text-red-500">{error}</span> : null}
        <div className="flex gap-2">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-900 dark:text-white">
              Min Timestamp
            </label>
            <input
              type="number"
              value={minTimestamp}
              onChange={(e) => setMinTimestamp(Number(e.target.value))}
              className="rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-gray-900 dark:text-white">
              Max Timestamp
            </label>
            <input
              type="number"
              value={maxTimestamp}
              onChange={(e) => setMaxTimestamp(Number(e.target.value))}
              className="rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
            />
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => {
              setMinTimestamp(Date.now() - 1000 * 60 * 60 * 1);
              setMaxTimestamp(Date.now());
            }}
            className="cursor-pointer rounded-lg bg-blue-500 p-2.5 text-white hover:bg-blue-600"
          >
            Past Hour
          </button>
          <button
            onClick={() => {
              setMinTimestamp(Date.now() - 1000 * 60 * 60 * 4);
              setMaxTimestamp(Date.now());
            }}
            className="cursor-pointer rounded-lg bg-blue-500 p-2.5 text-white hover:bg-blue-600"
          >
            Past 4 Hours
          </button>
          <button
            onClick={() => {
              const today = new Date();
              today.setHours(0, 0, 0, 0);
              setMinTimestamp(today.getTime());
              setMaxTimestamp(Date.now());
            }}
            className="cursor-pointer rounded-lg bg-blue-500 p-2.5 text-white hover:bg-blue-600"
          >
            Today
          </button>
          <button
            onClick={() => {
              setMinTimestamp(Date.now() - 1000 * 60 * 60 * 24 * 2);
              setMaxTimestamp(Date.now());
            }}
            className="cursor-pointer rounded-lg bg-blue-500 p-2.5 text-white hover:bg-blue-600"
          >
            Last 2 Days
          </button>
        </div>
        <div className="flex gap-2 items-center">
          <input type="checkbox" onChange={(e) => setRefreshEnabled(e.target.checked)} />
          <label>Auto Refresh</label>
        </div>
        {tableData?.map((table) => {
          return (
            <div key={table.tableName} className="flex w-full flex-col gap-2">
              <span>{table.tableName}</span>

              <Graph data={table.data} />
            </div>
          );
        })}
      </div>
    </main>
  );
}

export default Presentation;
