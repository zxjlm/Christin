import TableDataManagement from '@/components/TableDataManagement'
import {PageHeaderWrapper} from "@ant-design/pro-layout";

export default () => {
  return <PageHeaderWrapper>
    <TableDataManagement modelName={'Herb'}/>
  </PageHeaderWrapper>
}
