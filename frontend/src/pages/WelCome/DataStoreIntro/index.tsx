import styles from "./index.less";
import {Card, Statistic} from "antd";
import type {dataItemsState} from "@/pages/Welcome";

export default ({dataItems}: { dataItems: dataItemsState[] }) => {

  return <div className={styles.container}>
    <div id="components-card-demo-basic">
      <div>
        <Card
          title="数据存量"
          headStyle={{backgroundColor:"lightgray"}}
        >
          {dataItems.map(item => <Statistic key={item.name} title={item.name} value={item.value}/>)}
        </Card>
      </div>
    </div>
  </div>
};
