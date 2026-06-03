import './App.css'
import {useEffect, useState} from "react";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import {api, carregarEndpoints, setApiToken} from "./services/api.js";

function App() {
    const [endpoints, setEndpoints] = useState([]);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(null);

    useEffect(() => {
        async function verificarToken() {
            const tokenSalvo = localStorage.getItem("token");
            if (!tokenSalvo) {
                setLoading(false);
                return;
            }
            try {
                setApiToken(tokenSalvo);
                await api.get("/scripts/listar");
                const lista = await carregarEndpoints();
                setEndpoints(lista);
                setToken(tokenSalvo);
            } catch {
                localStorage.removeItem("token");
            } finally {
                setLoading(false);
            }
        }
        verificarToken();
    }, []);
    if (loading) {
        return <div className="loading">Carregando...</div>;
    }
    return (
        <div className="app">
            <div className="main-box">
                {token ?
                    <Dashboard token={token} endpoints={endpoints}/>:
                    <Login onLogin={setToken} setEndpoints={setEndpoints}/>
                }
            </div>
        </div>
    );
}
export default App;