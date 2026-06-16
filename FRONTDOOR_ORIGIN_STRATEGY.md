# Front Door Origin Strategy

Last updated: 2026-06-16

## Non-Prod Ownership

- `nonprod-shared` owns the entire non-prod Front Door stack
- `dev` and `staging` must not mutate shared Front Door resources directly

## Dev/Staging Output Contract

Example outputs:

- `frontend_origin_hostname`
- `frontend_origin_host_header`
- `frontend_health_probe_path`
- `api_origin_hostname`
- `api_origin_host_header`
- `api_health_probe_path`
- `gateway_public_fqdn`

## Example Remote State Pattern

```hcl
data "terraform_remote_state" "dev" {
  backend = "azurerm"
  config = {
    key = "dev.tfstate"
  }
}
```

`nonprod-shared` should consume env outputs and build origins/routes from them.

## Origin Group Strategy

- separate frontend and API origin groups
- allow dev and staging origins to be attached independently
- keep health probes and host headers explicit per route family

## Route Strategy

- route by hostname and/or path based on shared non-prod design
- preserve clean separation between frontend and API traffic

## WAF / Security Policy Strategy

- centralize WAF and security policy attachment in the Front Door owner state
- avoid per-env states attaching policies to shared routes

## Prod Strategy

- prod Front Door lives in `envs/prod`
- prod owns its own routes, origins, policies, and domain bindings

## Validation Checklist

- confirm dev/staging outputs exist
- confirm `nonprod-shared` reads them without cycles
- confirm only one state manages each Front Door object
- confirm route/origin health settings match kGateway exposure
