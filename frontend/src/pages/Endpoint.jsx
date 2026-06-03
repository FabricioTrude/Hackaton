import React from 'react';
import {executarEndpoint, resolveRef} from "../services/api.js";

const Endpoint = ({selectedEndpoint, formData, setFormData, error, result, setResult, setError}) => {
    const params = selectedEndpoint?.schema?.params || [];
    const required = selectedEndpoint?.schema?.body?.required || [];
    console.log(params, required)

    async function executar() {
        try {
            setError(null);
            setResult(null);
            const res = await executarEndpoint(selectedEndpoint, formData);
            setResult(res.data);
        } catch (err) {
            setError(err?.response?.data || err.message);
        }
    }
    return <div className="endpoint-wrapper">
        {!selectedEndpoint ? ( <div className="empty-state">Selecione um endpoint </div>) : (<>
        <div className="endpoint-input-wrapper">
            <div className="endpoint-header">
                <h2 id="endpoint-summary-name">{selectedEndpoint.raw.summary}</h2>
                <p className="endpoint-path">{selectedEndpoint.path}</p>
                <span className={`method method-${selectedEndpoint.method}`}> {selectedEndpoint.method}</span>
            </div>
            <div className="endpoint-body-wrapper">
                {/* BODY */}
                <p className="endpoint-body-header">Parameters</p>
                {params && Object.keys(params).length > 0 && (
                    <div className="form-section">
                        {Object.entries(params).map(([key, param]) => {
                            const isFile = key === "file";
                            const isOptional = param?.default !== undefined;
                            return (<div key={key} className="form-field">
                                <label>{param.title}{!isOptional && <span style={{ color: "red" }}> *</span>}</label>
                                <input  type={isFile ? "file" : "text"} required={!isOptional} onChange={(e) => {
                                            setFormData({...formData, [key]: isFile ? e.target.files[0] : e.target.value});
                                }}/></div>
                            );
                        })}
                    </div>
                )}
                <button className="form-btn execute" onClick={executar}>Executar</button>
            </div>
        </div>
        <div className="endpoint-response-wrapper">
            <div className="response-box-wrapper stdout-wrapper">
                <p className="response-title stdout">STDOUT</p>
                <div className="response-box stdout">
                    {result && (<pre>{JSON.stringify(result, null, 2)}</pre>)}
                </div>
            </div>
            <div className="response-box-wrapper stderr-wrapper">
                <p className="response-title stderr">STDERR</p>
                <div className="response-box stderr">
                    {error && (<pre>{JSON.stringify(error, null, 2)}</pre>)}
                </div>
            </div>
        </div>
        </>
        )}

        {/*/!* RESULT *!/*/}

        {/*/!* ERROR *!/*/}

    </div>
};

export default Endpoint;
