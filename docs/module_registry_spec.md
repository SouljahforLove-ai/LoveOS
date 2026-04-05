# SoulJahForLoveOS — Module Registry Specification

The Module Registry defines how modules are discovered, loaded, and integrated.

## 1. Registry File
Located at:
```
/LoveOS/modules/registry.json
```

## 2. Module Entry Format
```
{
  "name": "module_name",
  "version": "1.0",
  "engine": "emotional | identity | mythic | sovereignty",
  "entrypoint": "path.to.module:main"
}
```

## 3. Loading Rules
- modules must be local  
- no network calls  
- no external dependencies  
- must respect sovereignty boundaries  

## 4. Security
Modules cannot override core engines.
