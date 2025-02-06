import { Fragment, useEffect, useState } from "react";
import type { CableModemData, TableData, TableName } from "../dataTypes";
import { isValidKey } from "../utils/typing";
import FlashableElement from "./FlashableElement";

const listTables = async () => {
	const response = await fetch("/api/listTables");
	const data: string[] = await response.json();
	return data;
};

const refreshTables = async (): Promise<CableModemData> => {
	const tables = await listTables();
	const tableDataMapPromises = tables.map(async (table) => {
		const response = await fetch(`/api/${table}`);
		const data = await response.json();
		// Create the discriminated object:
		return { tableName: table as TableName, data } as TableData;
	});

	return await Promise.all(tableDataMapPromises);
};

function App() {
	const [tableData, setTableData] = useState<CableModemData>();
	const [, setRefreshInterval] = useState<NodeJS.Timeout>();
	const [refreshCount, setRefreshCount] = useState(0);
	const [lastRefresh, setLastRefresh] = useState(new Date());

	useEffect(() => {
		const interval = setInterval(async () => {
			try {
				const data = await refreshTables();
				setTableData(data);
			} finally {
				setRefreshCount((prev) => prev + 1);
				setLastRefresh(new Date());
			}
		}, 1000);

		setRefreshInterval(interval);
		return () => clearInterval(interval);
	}, []);

	useEffect(() => {
		refreshTables().then(setTableData);
	}, []);

	return (
		<main className="fixed h-[100vh] w-[100vw] dark:bg-gray-800 dark:text-white overflow-auto">
			<div className=" p-10 flex flex-col overflow-auto gap-10">
				<div>Last refresh: {lastRefresh.toLocaleString()}</div>
				<div className="flex gap-1">
					<span>Refresh count:</span>
					<FlashableElement>{refreshCount}</FlashableElement>
				</div>

				{tableData?.map((table, index) => {
					const columns = Object.keys(table.data[0]);

					return (
						<Fragment key={index}>
							<div className="w-full flex flex-col gap-2">
								<div className="text-2xl font-bold">
									{table.tableName}
								</div>
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
															dependentVar={
																row[column]
															}
														>
															{row[column]}
														</FlashableElement>
													) : null
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

export default App;
