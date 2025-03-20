import AttachFileIcon from "@mui/icons-material/AttachFile";
import InputAdornment from "@mui/material/InputAdornment";
import IconButton from "@mui/material/IconButton";
import SendIcon from "@mui/icons-material/Send";
import OutlinedInput from "@mui/material/OutlinedInput";

export function render({model}) {
  const [autogrow] = model.useState("auto_grow")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [enter_sends] = model.useState("enter_sends")
  const [error_state] = model.useState("error_state")
  const [max_rows] = model.useState("max_rows")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [rows] = model.useState("rows")
  const [value_input, setValueInput] = model.useState("value_input")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  let props = {}
  if (autogrow) {
    props = {minRows: rows}
  } else {
    props = {rows}
  }

  const send = () => {
    model.send_msg(value_input)
    setValueInput("")
  }

  return (
    <OutlinedInput
      multiline
      color={color}
      disabled={disabled}
      endAdornment={
        <InputAdornment position="end">
          <IconButton
            color="primary"
            onClick={() => send()}
          >
            <SendIcon />
          </IconButton>
        </InputAdornment>
      }
      error={error_state}
      maxRows={max_rows}
      label={label}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if ((event.key === "Enter") && (enter_sends || event.ctrlKey || event.shiftKey)) {
          send()
        }
      }}
      placeholder={placeholder}
      value={value_input}
      variant={variant}
      fullWidth
      {...props}
    />
  )
}
