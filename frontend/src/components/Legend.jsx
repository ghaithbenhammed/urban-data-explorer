import { INDICATEURS } from "../config/indicateurs";

function Legend({ indicateur }) {
  const config = INDICATEURS[indicateur];

  let gradient = "";
  let leftLabel = "Faible";
  let rightLabel = "Élevé";

  switch (config.palette) {
    case "goodbad":
      gradient =
        "linear-gradient(to right, #d73027, #fc8d59, #fee08b, #91cf60, #1a9850)";
      break;

    case "risk":
      gradient =
        "linear-gradient(to right, #1a9850, #91cf60, #fee08b, #fc8d59, #d73027)";
      break;

    case "blue":
      gradient =
        "linear-gradient(to right, #dbeafe, #93c5fd, #60a5fa, #2563eb, #1e3a8a)";
      break;

    case "purple":
      gradient =
        "linear-gradient(to right, #ede9fe, #c4b5fd, #a78bfa, #7c3aed, #4c1d95)";
      break;

    case "orange":
      gradient =
        "linear-gradient(to right, #ffedd5, #fdba74, #fb923c, #ea580c, #9a3412)";
      break;

    default:
      gradient = "linear-gradient(to right, #d73027, #1a9850)";
  }

  return (
    <div className="legend">
      <span>{leftLabel}</span>

      <div
        className="legend-gradient"
        style={{
          background: gradient,
        }}
      />

      <span>{rightLabel}</span>
    </div>
  );
}

export default Legend;
