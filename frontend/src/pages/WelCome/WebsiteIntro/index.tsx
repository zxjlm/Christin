import styles from "./index.less";
import {Card} from "antd";

export default ({userNumbers}: { userNumbers: number }) => (
  <div className={styles.container}>
    <div id="components-card-demo-basic">
      <div>
        <Card
          title="网站信息"
          // extra={<a href="#">More</a>}
          // style={{width: 400}}
          headStyle={{backgroundColor:"lightgray"}}
        >
          <Card type="inner" title="简介">
            <p>CMKGLab(Chinese Medicine Know Graph Lab) 是中医药数据知识图谱平台.</p>
          </Card>
          <Card type="inner" title="一些开放数据">
            <p>现在为 <strong>{userNumbers}</strong> 位用户提供服务</p>
          </Card>
          <Card type="inner" title="第三方接口">
            <p>为了更方便地服务于科研人员,我们提供了符合API设计规范的第三方接口以供各位用户调用.</p>
            <a href={'/apidocs'}>visit api documents</a>
          </Card>
        </Card>
      </div>
    </div>
  </div>
);
