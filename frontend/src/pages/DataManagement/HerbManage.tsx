import TableDataManagement from '@/components/TableDataManagement'
import {PageHeaderWrapper} from "@ant-design/pro-layout";

export default () => {
  return <PageHeaderWrapper content={'目前不建议使用这个进行数据的编辑'}>
    <TableDataManagement modelName={'Herb'}/>
  </PageHeaderWrapper>
}
