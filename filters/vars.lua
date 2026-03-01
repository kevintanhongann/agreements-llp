local vars = {}

function Meta(meta)
  for k, v in pairs(meta) do
    -- Store just the base value as a string
    vars[string.upper(k)] = pandoc.utils.stringify(v)
  end
end

function Str(el)
  -- Pattern %${(.-)} matches ${VARNAME}
  -- We use a function inside gsub to look up the match in our 'vars' table
  el.text = el.text:gsub("${(.-)}", function(name)
    local upper_name = string.upper(name)
    return vars[upper_name] or "${" .. name .. "}"
  end)
  return el
end

-- Return the filters in order: first collect metadata, then replace text
return {{Meta = Meta}, {Str = Str}}
