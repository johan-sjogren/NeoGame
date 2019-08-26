import {Hand} from './Hand';
import {Table} from './Table';

function Opponent () {
  return (
    <div>
      <Hand />
      <Table />
      This is the Opponent, containing a hand and a table
    </div>
  )
}

export default Opponent;