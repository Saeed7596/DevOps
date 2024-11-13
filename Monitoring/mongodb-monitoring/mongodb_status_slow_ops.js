var slow_ops = db.currentOp()["inprog"].filter(
   r =>
      r.op != "none" &&
      r.microsecs_running > 200000 &&
      !r.command?.hello &&
      r.command["$db"] != "admin"
);

print(JSON.stringify({ slow_ops }));
