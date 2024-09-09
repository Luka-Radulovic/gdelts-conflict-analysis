import express from 'express';
import path from 'path';
import open from 'open';

const app = express();
const port = 3000;

app.use(express.static(path.join(process.cwd())));

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
  open(`http://localhost:${port}`);
});
