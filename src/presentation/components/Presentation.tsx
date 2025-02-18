import { useState } from "react";
import type { CableModemData, Table, TableName } from "../dataTypes";
import { useInterval } from "../hooks/useInterval";
import Graph from "./Graph";

const listTables = async (): Promise<TableName[]> => {
  const response = await fetch("/api/tables");
  const data: string[] = await response.json();
  return data as TableName[];
};

const loadTables = async (): Promise<CableModemData> => {
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
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const reloadData = async () => {
    if (busy) {
      return;
    }

    try {
      const tableData = await loadTables();
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
  };

  useInterval(reloadData, 1000);

  return (
    <main className="fixed h-[100vh] w-[100vw] overflow-auto dark:bg-gray-800 dark:text-white">
      <div className="flex flex-col gap-10 overflow-auto p-10">
        {error ? <span className="text-red-500">{error}</span> : null}
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
