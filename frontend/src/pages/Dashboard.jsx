import { useState, useEffect } from "react";
import {resolveRef} from "../services/api.js";
import Endpoint from "./Endpoint.jsx";

const Dashboard = ({ token, endpoints }) => {
    const [selectedEndpoint, setSelectedEndpoint] = useState(null);
    const [formData, setFormData] = useState({});
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    if (!endpoints || endpoints.length === 0) {
        return <div>Carregando...</div>;
    }

    const grupos = endpoints.reduce((acc, endpoint) => {
        if (!acc[endpoint.categoria]) {
            acc[endpoint.categoria] = [];
        }
        acc[endpoint.categoria].push(endpoint);
        return acc;
    }, {});

    useEffect(() => {
        if (!selectedEndpoint) return;

        setResult(null);
        setError(null);

        const rawBody =
            selectedEndpoint?.raw?.requestBody?.content?.["application/json"]?.schema ||
            selectedEndpoint?.raw?.requestBody?.content?.["multipart/form-data"]?.schema;

        const resolvedBody =
            rawBody?.$ref
                ? resolveRef(rawBody.$ref, selectedEndpoint.components)
                : rawBody;

        const bodyProps = resolvedBody?.properties || {};

        const initialData = Object.keys(bodyProps).reduce((acc, key) => {
            acc[key] = "";
            return acc;
        }, {});

        setFormData(initialData);
    }, [selectedEndpoint]);
    return (
        <div id="dashboard">
            <h1 className="title">Dashboard</h1>

            <div className="dashboard-wrapper">

                {/* SIDEBAR */}
                <div className="sidebar">
                    {Object.entries(grupos).map(([categoria, endpoints]) => (
                        <div key={categoria} className="categoria">
                            <p className="categoria-title">{categoria}</p>

                            {endpoints.map(endpoint => (
                                <p
                                    key={endpoint.path + endpoint.method}
                                    onClick={() => setSelectedEndpoint(endpoint)}
                                    className={`endpoint ${
                                        selectedEndpoint?.path === endpoint.path &&
                                        selectedEndpoint?.method === endpoint.method
                                            ? "active"
                                            : ""
                                    }`}
                                >
                                    # {endpoint.nome} ({endpoint.method})
                                </p>
                            ))}
                        </div>
                    ))}
                </div>

                {/* MAIN PANEL */}
                {<Endpoint
                    selectedEndpoint={selectedEndpoint}
                    formData={formData}
                    setFormData={setFormData}
                    error={error}
                    result={result}
                    setError={setError}
                    setResult={setResult}
                />}
            </div>
        </div>
    );
};

export default Dashboard;