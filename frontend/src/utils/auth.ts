export const getUserId = () : string | null => {
  const user_id = localStorage.getItem('user_id')
  if (!user_id) {
    console.error('User not logged in')
    return null
  }
  return user_id
}