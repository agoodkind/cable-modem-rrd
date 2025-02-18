import { Fragment, useEffect, useState } from "react";
import type { CableModemData, Table, TableName } from "../dataTypes";
import { isValidKey } from "../utils/typing";
import FlashableElement from "./FlashableElement";
import Graph from "./Graph";

const listTables = async (): Promise<TableName[]> => {
  const response = await fetch("/api/tables");
  const data: string[] = await response.json();
  return data as TableName[];
};

const refreshTables = async (): Promise<CableModemData> => {
  const tables = await listTables();
  const tableDataMapPromises = tables.map(async (table) => {
    const response = await fetch(`/api/tables/${table}`);
    const data = await response.json();
    // Create the discriminated object:
    return { tableName: table as TableName, data } as Table;
  });

  return await Promise.all(tableDataMapPromises);
};

function Presentation() {
  const [tableData, setTableData] = useState<CableModemData>();

  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshCount, setRefreshCount] = useState(0);
  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [refreshSpeed, setRefreshSpeed] = useState(2000);

  const [isScraping, setIsScraping] = useState(false);
  const [lastScrape, setLastScrape] = useState(new Date());
  const [rescapeSpeed, setRescapeSpeed] = useState(0);
  const [scrapeError, setScrapeError] = useState<string>();

  const scrapeNewData = async () => {
    if (isScraping) {
      return;
    }
    setScrapeError(undefined);
    setIsScraping(true);
    try {
      await fetch("/api/scrape", { method: "POST" });
      await refreshTables().then(setTableData);
    } catch (error) {
      if (error instanceof Error) {
        setScrapeError(error.message);
      } else {
        setScrapeError(JSON.stringify(error));
      }
    } finally {
      setIsScraping(false);
      setLastScrape(new Date());
    }
  };

  useEffect(() => {
    if (!rescapeSpeed) {
      return;
    }

    const interval = setInterval(async () => {
      await scrapeNewData();
    }, rescapeSpeed);

    return () => clearInterval(interval);
  }, [rescapeSpeed]);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (isRefreshing || !refreshSpeed || isScraping) {
        return;
      }
      try {
        setIsRefreshing(true);
        const data = await refreshTables();
        setTableData(data);
      } finally {
        setRefreshCount((prev) => prev + 1);
        setLastRefresh(new Date());
        setIsRefreshing(false);
      }
    }, refreshSpeed);

    return () => clearInterval(interval);
  }, [refreshSpeed]);

  useEffect(() => {
    refreshTables().then(setTableData);
  }, []);

  return (
    <main className="fixed h-[100vh] w-[100vw] overflow-auto dark:bg-gray-800 dark:text-white">
      <div className="flex flex-col gap-10 overflow-auto p-10">
        <div className="flex flex-col items-start gap-2">
          <div>Last refresh: {lastRefresh.toLocaleString()}</div>
          <div className="flex flex-col gap-1">
            {scrapeError && (
              <div className="flex gap-1 text-red-500">
                <span>Scrape Error:</span>
                <FlashableElement>{scrapeError}</FlashableElement>
              </div>
            )}
            <div className="flex gap-1">
              <span>Rescrape Speed:</span>
              <input
                type="number"
                id="number-input"
                className="w-fit rounded-lg border border-gray-300 bg-gray-50 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                value={rescapeSpeed}
                onChange={(e) => setRescapeSpeed(Number(e.target.value))}
                required
              />
            </div>
            <div className="flex gap-1">
              <span>Refresh Speed:</span>
              <input
                type="number"
                id="number-input"
                className="w-fit rounded-lg border border-gray-300 bg-gray-50 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
                value={refreshSpeed}
                onChange={(e) => setRefreshSpeed(Number(e.target.value))}
                required
              />
            </div>
            <div className="flex gap-1">
              <span>Refresh count:</span>
              <FlashableElement>{refreshCount}</FlashableElement>
            </div>
          </div>
          <div className="flex gap-1">
            <span>Last scrape:</span>
            <FlashableElement as="span" className="w-fit">
              {lastScrape.toLocaleString()}
            </FlashableElement>
          </div>
          <button
            onClick={scrapeNewData}
            disabled={isScraping}
            className="cursor-pointer rounded border p-1 active:bg-gray-300 active:text-black"
          >
            {isScraping ? "Scraping...." : "Scrape New Data"}
          </button>
        </div>
        {tableData?.map((table) => {
          return (
            <div key={table.tableName} className="flex w-full flex-col gap-2">
              <span>{table.tableName}</span>

              <Graph data={table.data} />
            </div>
          );
        })}

        {tableData?.map((table, index) => {
          const columns = Object.keys(table.data[0]);

          return (
            <Fragment key={index}>
              <div className="flex w-full flex-col gap-2">
                <div className="text-2xl font-bold">{table.tableName}</div>
                <table className="table-fixed divide-y">
                  <thead>
                    <tr>
                      {columns.map((column, index) => (
                        <th key={index}>{column}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {table.data.map((row, index) => (
                      <tr key={index}>
                        {columns.map((column, index) =>
                          isValidKey(column, row) ? (
                            <FlashableElement
                              as="td"
                              className="border p-1"
                              key={index}
                              dependentVar={row[column]}
                            >
                              {row[column]}
                            </FlashableElement>
                          ) : null,
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Fragment>
          );
        })}
      </div>
    </main>
  );
}

export default Presentation;
