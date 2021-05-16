import styles from "./index.less";
import {Card, Statistic} from "antd";
import {useEffect, useState} from "react";
import {projectRuntime} from "@/services/site-data/api";

interface projectNumberState {
  status: string
  numbers: number
}

const statusMapper = {
  'creating': '创建中',
  'running': '运行中',
  'exited': '休眠中',
  'deleted': '已删除',
}

export default () => {
  const [projectNumbers, setProjectNumbers] = useState<projectNumberState[]>([]);

  useEffect(() => {
    projectRuntime().then(response => {
      const tmp = Object.entries(response).map(item => ({'status': statusMapper[item[0]], 'numbers': item[1].length}))
      setProjectNumbers(tmp)
    })
  }, []);

  return <div className={styles.container}>
    <div id="components-card-demo-basic">
      <div>
        <Card
          title="项目情况"
          headStyle={{backgroundColor:"lightgray"}}
        >
          {projectNumbers.map(item => <Statistic key={item.status} title={item.status} value={item.numbers}/>)}
        </Card>
      </div>
    </div>
  </div>
};
