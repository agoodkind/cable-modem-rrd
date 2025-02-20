// import {
//     CategoryScale,
//     Chart as ChartJS,
//     Legend,
//     LinearScale,
//     LineElement,
//     PointElement,
//     Title,
//     Tooltip,
// } from "chart.js";
// import faker from "faker";
// import { Line } from "react-chartjs-2";
// import type { TableData } from "../dataTypes";

// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   PointElement,
//   LineElement,
//   Title,
//   Tooltip,
//   Legend,
// );

// export const options = {
//   responsive: true,
//   plugins: {
//     legend: {
//       position: "top" as const,
//     },
//     title: {
//       display: true,
//       text: "Chart.js Line Chart",
//     },
//   },
// };

// // const labels = ["Channel 1", ...];
// const times = [1,2,3,4,5]; //....


// /**
//  * 
//  */

// export const data = {
//   labels,
//   datasets: [
//     {
//       label: "Dataset 1",
//         //   data: // for each timestamp get the SNR, power, or whatever value
//           data: [9, 7, 3, 5, 2],
//       borderColor: "rgb(255, 99, 132)",
//       backgroundColor: "rgba(255, 99, 132, 0.5)",
//     },
//     {
//       label: "Dataset 2",
//       data: labels.map(() => faker.datatype.number({ min: -1000, max: 1000 })),
//       borderColor: "rgb(53, 162, 235)",
//       backgroundColor: "rgba(53, 162, 235, 0.5)",
//     },
//   ],
// };

// const getDataset = (data: TableData[], channel: number)  => { }

// export function Chart<T extends TableData>({ data }: { data: T[] }) {

    

    
      
//   return <Line options={options} data={data} />;
// }
