import {useState} from "react";
import {
    api,
    carregarEndpoints,
    setApiToken
} from "../services/api.js";

function Login({ onLogin, setEndpoints }) {

    const [token, setToken] = useState("");
    const [erro, setErro] = useState("");

    async function entrar() {
        try {
            setApiToken(token);
            await api.get("/scripts/listar");
            const lista = await carregarEndpoints();
            localStorage.setItem("token", token);
            setEndpoints(lista);
            onLogin(token);
        } catch (err) {
            setErro("Token inválido");
            console.error(err);
        }
    }

    return (
        <div id="login">
            <h1 className="title">Hackaton</h1>
            <input
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Insira o token"
            />
            <button onClick={entrar}>
                Entrar
            </button>
            {erro && <p>{erro}</p>}
        </div>
    );
}

export default Login;