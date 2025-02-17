import type { TooltipProps } from "recharts";
import type {
  NameType,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";

export const ChartTooltip = ({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) => {
  if (!active || !payload || !payload.length) {
    return null;
  }
  return (
    <div className="max-h-80 rounded bg-white p-2 dark:bg-gray-800">
      <div className="text-lg font-bold">{label}</div>
      {payload.map((entry, index) => (
        <div key={`item-${index}`} style={{ color: entry.color }}>
          {`${entry.name} : ${entry.value}`}
        </div>
      ))}
    </div>
  );
};
