function Sidebar({
  mode,
  setMode,
  indicateur,
  setIndicateur,
  arrondissement,
  setArrondissement,
  compareArrondissement,
  setCompareArrondissement,
}) {
  const changeMode = (newMode) => {
    setMode(newMode);

    if (newMode === "acheter") {
      setIndicateur("prix-median");
    }

    if (newMode === "investir") {
      setIndicateur("rentabilite");
    }

    if (newMode === "habiter") {
      setIndicateur("qualite-vie");
    }

    if (newMode === "vieillir") {
      setIndicateur("vieillissement");
    }
  };

  return (
    <div className="sidebar">
      <h2>Mode analyse</h2>

      <div className="mode-buttons">
        <button
          className={mode === "acheter" ? "active" : ""}
          onClick={() => changeMode("acheter")}
        >
          Acheter
        </button>

        <button
          className={mode === "investir" ? "active" : ""}
          onClick={() => changeMode("investir")}
        >
          Investir
        </button>

        <button
          className={mode === "habiter" ? "active" : ""}
          onClick={() => changeMode("habiter")}
        >
          Habiter
        </button>

        <button
          className={mode === "vieillir" ? "active" : ""}
          onClick={() => changeMode("vieillir")}
        >
          Vieillir
        </button>
      </div>

      <hr />

      {/* ACHETER */}

      {mode === "acheter" && (
        <>
          <h3>Indicateur</h3>

          <div className="submenu">
            <button className="active">Prix médian</button>
          </div>
        </>
      )}

      {/* INVESTIR */}

      {mode === "investir" && (
        <>
          <h3>Indicateur</h3>

          <div className="submenu">
            <button
              className={indicateur === "rentabilite" ? "active" : ""}
              onClick={() => setIndicateur("rentabilite")}
            >
              Rentabilité
            </button>

            <button
              className={indicateur === "tension" ? "active" : ""}
              onClick={() => setIndicateur("tension")}
            >
              Tension immobilière
            </button>

            <button
              className={indicateur === "prix-median" ? "active" : ""}
              onClick={() => setIndicateur("prix-median")}
            >
              Evolution des prix
            </button>
          </div>
        </>
      )}

      {/* HABITER */}

      {mode === "habiter" && (
        <>
          <h3>Indicateur</h3>

          <div className="submenu">
            <button
              className={indicateur === "qualite-vie" ? "active" : ""}
              onClick={() => setIndicateur("qualite-vie")}
            >
              Qualité de vie
            </button>

            <button
              className={indicateur === "securite" ? "active" : ""}
              onClick={() => setIndicateur("securite")}
            >
              Sécurité
            </button>

            <button
              className={indicateur === "air" ? "active" : ""}
              onClick={() => setIndicateur("air")}
            >
              Pollution
            </button>

            <button
              className={indicateur === "transport" ? "active" : ""}
              onClick={() => setIndicateur("transport")}
            >
              Transport
            </button>
          </div>
        </>
      )}

      {/* VIEILLIR */}

      {mode === "vieillir" && (
        <>
          <h3>Indicateur</h3>

          <div className="submenu">
            <button className="active">Score vieillissement</button>
          </div>
        </>
      )}

      <hr />

      <h3>Arrondissement</h3>

      <select
        value={arrondissement}
        onChange={(e) => setArrondissement(e.target.value)}
      >
        <option value="all">Tous</option>

        {[...Array(20)].map((_, i) => (
          <option key={i + 1} value={i + 1}>
            {i + 1}e
          </option>
        ))}
      </select>
      <hr />

      <h3>Comparer avec</h3>

      <select
        value={compareArrondissement}
        onChange={(e) => setCompareArrondissement(e.target.value)}
      >
        <option value="all">Aucun</option>

        {[...Array(20)].map((_, i) => {
          const value = String(i + 1);

          if (value === arrondissement) return null;

          return (
            <option key={value} value={value}>
              {value}e
            </option>
          );
        })}
      </select>
    </div>
  );
}

export default Sidebar;
