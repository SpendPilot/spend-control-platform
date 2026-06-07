{{- define "business-ai-app.namespace" -}}
{{- .Values.namespace.name -}}
{{- end -}}

{{- define "business-ai-app.name" -}}
spend-control
{{- end -}}

{{- define "business-ai-app.serviceAccountName" -}}
{{- .Values.serviceAccount.name -}}
{{- end -}}
