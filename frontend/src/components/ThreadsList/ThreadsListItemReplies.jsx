import React from "react"

const ThreadsListItemReplies = ({ thread }) => (
  <span className="threads-list-item-replies"
    title={interpolate(
      ngettext("%(replies)s reply", "%(replies)s replies", thread.replies),
      {replies: thread.replies},
      true
    )}
  >
    <span className="material-icon">chat_bubble_outline</span>
    {thread.replies > 980 ? Math.round(thread.replies / 1000) + "K" : thread.replies}
  </span>
)

export default ThreadsListItemReplies