import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

function ParcPanel({ data }) {
  if (!data || data.length === 0) return null;

  const colors = ["#1d4ed8", "#60a5fa", "#bfdbfe"];

  const getLabel = (categorie) => {
    if (categorie === "petit") return "< 40 m²";

    if (categorie === "moyen") return "40 - 80 m²";

    if (categorie === "grand") return "> 80 m²";

    return categorie;
  };

  const chartData = data.map((item) => ({
    ...item,
    label: getLabel(item.categorie_surface),
  }));

  return (
    <div className="parc-panel">
      <h2>Typologie des logements</h2>

      <p className="parc-subtitle">
        Répartition des logements selon leur surface.
      </p>

      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="pourcentage"
            nameKey="label"
            innerRadius={55}
            outerRadius={90}
            paddingAngle={3}
            label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
          >
            {chartData.map((entry, index) => (
              <Cell key={index} fill={colors[index % colors.length]} />
            ))}
          </Pie>

          <Tooltip formatter={(value) => `${value.toFixed(1)} %`} />

          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ParcPanel;
