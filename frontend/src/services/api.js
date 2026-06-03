import axios from 'axios';
import endpoint from "../pages/Endpoint.jsx";

export const api = axios.create({
    baseURL: 'http://127.0.0.1:8000'
});

export function setApiToken(token) {
    api.defaults.headers.common["X-Isy-Token"] = token;
}

const EXCLUDED_ENDPOINTS = [
    "/",
    "/openapi.json",
    "/docs",
    "/redoc",
];

export async function carregarEndpoints() {
    const response = await api.get("/openapi.json");
    const paths = response.data.paths;

    const lista = [];

    for (const [path, methods] of Object.entries(paths)) {
        if (path === "/" || path === "/openapi.json") continue;

        const partes = path.split("/").filter(Boolean);
        const categoria = partes[0] || "geral";
        const nome = partes[1] || partes[0];
        const process = (method, methodName) => {
            if (!method) return;
            const bodySchema =
                method?.requestBody?.content?.["application/json"]?.schema ||
                method?.requestBody?.content?.["multipart/form-data"]?.schema ||
                null;
            const resolvedBody = method?.requestBody?.$ref ? resolveRef(method?.requestBody.$ref, response.data.components) : method?.requestBody;
            const operationId = method?.operationId;
            const parameters = response.data.components.schemas[`Body_${operationId}`]
            // console.log(parameters)
            lista.push({
                categoria,
                nome,
                path,
                method: methodName.toUpperCase(),
                schema: {
                    body: resolvedBody || {},
                    params: parameters?.properties || {},
                },

                raw: method
            });
        };

        process(methods.get, "get");
        process(methods.post, "post");
        process(methods.put, "put");
        process(methods.delete, "delete");
    }

    return lista;
}

export async function executarEndpoint(endpoint, formData) {
    const url = endpoint.path;
    const method = endpoint.method.toLowerCase();

    const hasFile = Object.values(formData).some(v => v instanceof File);

    if (hasFile) {
        const fd = new FormData();

        Object.entries(formData).forEach(([k, v]) => {
            if (v !== "" && v != null) fd.append(k, v);
        });

        return api.request({
            url,
            method,
            data: fd
        });
    }

    // FORM ENCODED (SEU CASO PRINCIPAL)
    const body = new URLSearchParams();

    Object.entries(formData).forEach(([k, v]) => {
        if (v !== "" && v != null) {
            body.append(k, v);
        }
    });

    return api.request({
        url,
        method,
        data: body,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    });
}

export function resolveRef(ref, components) {
    if (!ref) return null;
    const key = ref.replace("#/components/schemas/", "");
    return components?.schemas?.[key] || null;
}